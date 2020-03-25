# encoding=utf8

import acceptor
import loop


class TcpServer(object):
    """
    tcp server
    """

    def __init__(self, host_addr, time_out):
        self._host_addr = host_addr
        self.loop = loop.EventLoop(time_out)

        self.acceptor = acceptor.Acceptor(self.loop, host_addr)
        self.acceptor.set_new_connection_callback(self.new_connection)

        self.conn_map = {}  # 连接的管理

    def run(self):
        self.loop.is_running = True
        self.loop.loop()

    def new_connection(self, conn_socket, peer_host):
        """
        accpet到新连接的回调函数
        """
        import time, tcp_connection
        conn_key = '{}#{}#{}'.format(str(self._host_addr),str(peer_host),str(time.time()))  # 四元组 + 时间戳
        conn = tcp_connection.TcpConnection(self.loop, conn_socket, conn_key)
        conn.set_close_callback(self.remove_connection)  # 指定打开操作
        conn.set_message_callback(self.on_message)
        conn.set_write_complete_callback(self.write_complete)

        self.conn_map[conn] = conn

    def remove_connection(self, connection):
        conn_key = connection.conn_key
        if not conn_key in self.conn_map:
            return
        del self.conn_map[conn_key]

    def on_message(self, tcp_connection, buffer):
        """
        消息到来
        """
        raise NotImplementedError

    def write_complete(self):
        """
        消息发送完毕
        """
        raise NotImplementedError