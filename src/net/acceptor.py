# encoding=utf8

from src.net.channel import Channel
from src.net.socket_warp import ServerSocket


class Acceptor(object):
    """
    server listen socket
    """

    def __init__(self, loop, host_addr):
        self._loop = loop
        self.socket = ServerSocket()
        self.socket.bind_and_listen(host_addr)

        self.accept_channel = Channel(loop, self.socket.fd)
        self.accept_channel.add_loop()  # 添加到poller中

        self.accept_channel.set_read_callback(self.handle_read)
        self.accept_channel.need_read = True
        self.accept_channel.set_error_callback(self.handle_error)

        self.new_connection_callback = None  # accept到新连接执行此回调

    def set_new_connection_callback(self, method):
        # server 连接建立执行的回调
        self.new_connection_callback = method

    def handle_read(self):
        """
        accept 到一个新client socket，执行callback，最终会注册到poller中
        """
        conn_socket, peer_host = self.socket.accept()

        if self.new_connection_callback and conn_socket is not None and peer_host is not None:
            self.new_connection_callback(conn_socket, peer_host)

    def handle_error(self):
        LOG.error('acceptor error')
