# encoding=utf8
from src.net.channel import Channel
from src.net.socket_warp import ClientSocket

class ConnectorState(object):
    """
    执行非阻塞connect 过程中 的状态
    """
    CONNECTED = 0
    CONNECTING = 1
    ERROR = 2


class Connector(object):
    """
    client socket的连接器
    """

    def __init__(self, loop):
        self._loop = loop
        self.socket = ClientSocket()
        self.conn_channel = Channel(loop, self.socket.fd)
        self.conn_channel.add_loop()

        self.conn_channel.set_write_callback(self.handle_write)
        self.conn_channel.set_error_callback(self.handle_error)

        self.new_conn_callback = None  # 连接建立成功时的回调
        self.dist_address = None  # 远程地址

    def connect(self, dist_address):
        self.dist_address = dist_address
        conn_state = self.socket.connect(dist_address)  # 连接server

        if conn_state == ConnectorState.CONNECTING:
            # 连接正在建立，需要设置对socket写的监控
            self.conn_channel.need_write = True
        elif conn_state == ConnectorState.CONNECTED:
            # 连接建立成功
            self.new_conn_callback(self.socket)
            LOG.info('连接：' + str(dist_address) + '成功！')
        else:
            LOG.error('连接：' + str(dist_address) + '失败！')

        return conn_state

    def handle_write(self):

        # 能够获得对端host，即代表连接建立成功
        peer_addr, is_success = self.socket.get_peer_name()
        if is_success:
            # 关闭channel的全部监听，不同于acceptor会一直监听
            self.conn_channel.disable()
            # 从poller的map中删除
            self.conn_channel.close()
            self.new_conn_callback(self.socket.sock, peer_addr)
            LOG.info('连接：' + str(peer_addr) + '成功！')

        else:
            # 连接建立失败
            self.handle_error()

    def handle_error(self):
        self.conn_channel.disable()
        # 从poller的map中删除
        self.conn_channel.close()
        LOG.error('连接：' + str(self.dist_address) + '失败！')

    def set_new_conn_callback(self, method):
        self.new_conn_callback = method
