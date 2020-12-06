# encoding=utf8
import time
from src.net.socket_warp import ClientSocket
from src.net.channel import Channel
from src.util.buffer import Buffer
from src.util.loop_deco import RunInLoop


class TcpConnectionState(object):
    CONNECTED = 0
    DISCONNECTING = 1
    DISCONNECTED = 2


class TcpConnection(object):
    """
    每一个client socket 对应一个tcp connection
    """

    def __init__(self, loop, conn_socket, conn_key):
        self._loop = loop
        self.conn_key = conn_key
        self.socket = ClientSocket(conn_socket)

        self.channel = Channel(loop, self.socket.fd)
        self.channel.add_loop()

        self.channel.set_read_callback(self.handle_read)
        self.channel.need_read = True
        self.channel.set_write_callback(self.handle_write)
        # LT 不能一直设置可写
        self.channel.need_write = False
        self.channel.set_error_callback(self.handle_error)

        self.read_buffer = Buffer()
        self.output_buffer = Buffer()

        self.state = TcpConnectionState.CONNECTED

        self.message_callback = None
        self.write_complete_callback = None
        self.close_callback = None

        # 上次接收到客户端心跳的时间
        self.last_recv_heart_time = time.time()

    @RunInLoop
    def send(self, data):
        # 发送数据（主动调用），不一定能发送完
        # 1）客户端往服务端发送消息；2）服务端消息分发
        from src.proto.msg.msg_codec import MsgCodec

        try:
            encode = MsgCodec()  # 自定义协议的编解码器
            data = encode.encode(data)  # 编码
        except Exception, e:
            LOG.error(e.message)
            return
        sent_count, is_close = self.socket.send(data)
        if is_close:
            self.handle_close()

        if sent_count < len(data):
            # 剩余为发送内容放入output_buffer
            self.output_buffer.append(data[sent_count:])
            self.channel.need_write = True
        elif sent_count == len(data) and self.write_complete_callback:
            # 发送完全
            self.write_complete_callback()

    @RunInLoop
    def shutdown(self):
        if self.state != TcpConnectionState.CONNECTED:
            return
        if self.channel.need_write:
            self.state = TcpConnectionState.DISCONNECTING
        else:
            self.handle_close()
            self.state = TcpConnectionState.DISCONNECTED

    def handle_read(self):
        """
        读就绪回调
        """
        from src.proto.msg.msg_codec import MsgCodec

        recv_data, is_close = self.socket.recv(65535)
        if is_close:
            self.handle_close()
            return

        self.read_buffer.append(recv_data)

        codec = MsgCodec()  # 自定义协议编解码器

        while True:
            try:
                command, packet = codec.decode(self.read_buffer)

                if not command and not packet:
                    break
                if self.message_callback:
                    # 消息就绪回调
                    self.message_callback(self, command, packet)
            except Exception, e:
                #  解码异常，关闭客户端连接
                LOG.error(e.message)
                self.handle_close()
                break

    def handle_write(self):
        """
        channel.need_write 时会被调用（数据为发送完全就会设置此回调在就绪的时候继续发送）
        """
        assert isinstance(self.output_buffer, Buffer)

        sent_data = self.output_buffer.get_all()
        sent_count, is_close = self.socket.send(sent_data)
        if is_close:
            self.handle_close()
        if sent_count == len(sent_data):
            self.channel.need_write = False  # 数据发送完全，关闭对该channel的监听
            self.output_buffer.add_read_index(sent_count)

            if self.write_complete_callback:
                self.write_complete_callback()

            if self.state == TcpConnectionState.DISCONNECTING:
                # channel 状态为带关闭
                self.handle_close()
                self.state = TcpConnectionState.DISCONNECTED
        else:
            self.output_buffer.add_read_index(sent_count)

    def handle_error(self):
        LOG.error('connection error while fd is listened by poller')
        self.handle_close()

    def handle_close(self):
        self.channel.disable()  # 关闭对channel的监听
        self.socket.close()

        if self.close_callback:
            self.close_callback(self)

        self.channel.close()  # 将channel从poller中移除
        self.state = TcpConnectionState.DISCONNECTED
        LOG.error('Client: ' + self.conn_key + ' close !')

    def set_close_callback(self, method):
        # connection_map中移除tcp_conn
        self.close_callback = method

    def set_message_callback(self, method):
        self.message_callback = method

    def set_write_complete_callback(self, method):
        self.write_complete_callback = method


