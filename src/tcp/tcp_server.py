# encoding=utf8

import acceptor
import loop
import logger


class TcpServer(object):
    """
    tcp server
    """

    def __init__(self, host_addr, time_out):
        self._host_addr = host_addr

        self._logger = logger.Logger()  # 日志服务，每一个线程一个

        self.loop = loop.EventLoop(time_out, self._logger)

        self.acceptor = acceptor.Acceptor(self.loop, host_addr, self._logger)
        self.acceptor.set_new_connection_callback(self.new_connection)

        self.conn_map = {}  # 连接的管理

        # 系统服务
        import sys_server
        self._sys_server = sys_server.SystemServer(self._logger, self.loop)

    def run(self):
        self.loop.is_running = True
        self.loop.loop()

    def new_connection(self, conn_socket, peer_host):
        """
        accept到新连接的回调函数
        """
        import time, tcp_connection
        conn_key = '{}#{}#{}'.format(str(self._host_addr), str(peer_host), str(time.time()))  # 四元组 + 时间戳
        conn = tcp_connection.TcpConnection(self.loop, conn_socket, conn_key, self._logger)
        conn.set_close_callback(self.remove_connection)  # 指定打开操作
        conn.set_message_callback(self.on_message)
        conn.set_write_complete_callback(self.write_complete)

        self.conn_map[conn_key] = conn
        self._logger.write_log('new conn' + str(peer_host), 'info')

    def remove_connection(self, connection):
        conn_key = connection.conn_key
        if not self.conn_map.has_key(conn_key):
            return
        del self.conn_map[conn_key]

    def heart_beat(self, internal=5):
        """
        注册服务端心跳服务
        """
        import sys_server
        heart_beat_server = sys_server.ServerHeartBeatServer(self._sys_server, self.conn_map, internal)
        heart_beat_server.register()

    def client_heart_beat_handler(self, tcp_connection, msg):
        """
        客户端心跳的处理函数
        """
        import time
        tcp_connection.last_recv_heart_time = time.time()
        # print tcp_connection.conn_key + " heart beat" + str(time.time())

    def on_message(self, tcp_connection, command, packet):
        """
        消息到来
        """
        raise NotImplementedError

    def write_complete(self):
        """
        消息发送完毕
        """
        raise NotImplementedError
