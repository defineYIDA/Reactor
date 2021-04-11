# encoding=utf8

from src.net.acceptor import Acceptor
from src.net.loop import EventLoop


class TcpServer(object):
    """
    tcp server
    """

    def __init__(self, host_addr, time_out):
        from src.util.logger import Logger
        self._host_addr = host_addr

        Logger.start_logger_service()  # 日志服务，每一个线程一个

        self.loop = EventLoop(time_out)

        self.acceptor = Acceptor(self.loop, host_addr)
        self.acceptor.set_new_connection_callback(self.new_connection)

        self.conn_map = {}  # 连接的管理

        # 系统服务
        from src.util.sys_server import SystemServer
        self._sys_server = SystemServer(self.loop)

    def run(self):
        self.loop.is_running = True
        self.loop.loop()

    def new_connection(self, conn_socket, peer_host):
        """
        accept到新连接的回调函数
        """
        import time, tcp_connection
        conn_key = '{}#{}#{}'.format(str(self._host_addr), str(peer_host), str(time.time()))  # 四元组 + 时间戳
        conn = tcp_connection.TcpConnection(self.loop, conn_socket, conn_key)

        conn.set_close_callback(self.remove_connection)  # 指定打开操作
        conn.set_write_complete_callback(self.write_complete)

        # 1 初始化channel的上下文 2 设置pipeline
        conn.ctx = self.init_channel(conn)

        self.conn_map[conn_key] = conn
        LOG.info('new conn ' + str(peer_host))

    def init_channel(self, conn):
        """初始化channel上下文"""
        from src.pipeline.pipeline import Pipeline
        from src.pipeline.channel_context import ChannelContext
        pipe = Pipeline()
        self.init_pipeline(pipe)
        ctx = ChannelContext(conn, pipe)
        return ctx

    def init_pipeline(self, pipe):
        """初始化pipeline，消息处理管道"""
        raise NotImplementedError

    def remove_connection(self, conn_key):
        if not self.conn_map.has_key(conn_key):
            return
        del self.conn_map[conn_key]

    def heart_beat(self, internal=5):
        """
        注册服务端心跳服务
        """
        from src.util.sys_server import ServerHeartBeatServer
        heart_beat_server = ServerHeartBeatServer(self._sys_server, self.conn_map, internal)
        heart_beat_server.register(self.send_heartbeat)

    def add_timer(self, timer):
        self.loop.add_timer(timer)
    
    def write_complete(self):
        pass

    def send_heartbeat(self, conn):
        pass
