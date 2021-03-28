# encoding=utf8


class TcpClient(object):
    """
    tcp client
    """

    def __init__(self, timeout):
        from src.net.loop import EventLoop
        from src.net.connector import Connector
        from src.util.logger import Logger

        Logger.start_logger_service()  # 日志服务，每一个线程一个
        self.loop = EventLoop(timeout)
        self.tcp_conn = None
        self.connector = Connector(self.loop)
        self.connector.set_new_conn_callback(self.new_connection)

    def run(self):
        self.loop.is_running = True
        self.loop.loop()

    def connect(self, dist_address):
        self.connector.connect(dist_address)

    def disconnect(self):
        if self.tcp_conn:
            self.tcp_conn.shutdown()

    def new_connection(self, conn_socket, peer_addr):
        import time
        import tcp_connection

        # client连接成功时调用
        conn_key = '{}#{}#{}'.format(str(conn_socket.getsockname()), str(peer_addr), str(time.time()))
        self.tcp_conn = tcp_connection.TcpConnection(self.loop, conn_socket, conn_key)

        self.tcp_conn.set_close_callback(self.on_connection_close)
        self.tcp_conn.set_write_complete_callback(self.write_complete)

        self.tcp_conn.ctx = self.init_channel(self.tcp_conn)
        self.on_connection_ready(self.tcp_conn)

    def init_channel(self, conn):
        """初始化channel上下文"""
        from src.pipeline.pipeline import Pipeline
        from src.pipeline.channel_context import ChannelContext
        pipe = Pipeline()
        self.init_pipeline(pipe)
        ctx = ChannelContext(conn, pipe)
        return ctx

    def send(self, data):
        if self.tcp_conn:
            self.tcp_conn.send(data)
        else:
            LOG.error('连接建立失败不能发送消息')

    def add_timer(self, timer):
        """添加计时器"""
        self.loop.add_timer(timer)

    def on_connection_close(self, connection):
        LOG.info('connection close', True)
        self.loop.is_running = False

    def init_pipeline(self, pipe):
        """初始化pipeline，消息处理管道"""
        raise NotImplementedError

    def on_connection_ready(self, conn):
        """连接就绪"""
        raise NotImplementedError


    def write_complete(self):
        """
        消息发送完毕
        """
        pass
