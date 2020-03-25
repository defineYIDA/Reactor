# encoding=utf8

import channel
from socket_warp import ServerSocket


class Acceptor(object):
    """
    server listen socket
    """

    def __init__(self, loop, host_addr):
        self._loop = loop
        self.socket = ServerSocket()
        self.socket.bind_and_listen(host_addr)

        self.accept_channel = channel.Channel(loop, self.socket.fd)
        self.accept_channel.add_loop()  # 添加到poller中
        self.accept_channel.set_read_callback(self.handle_read)
        self.accept_channel.need_read = True

        self.new_connection_callback = None  # accpet到新连接执行此回调

    def set_new_connection_callback(self, method):
        # server 连接建立执行的回调
        self.new_connection_callback = method

    def handle_read(self):
        """
        accpet 到一个新client socket，执行callback，最终会注册到poller中
        """
        conn_socket = None
        peer_host = None
        conn_socket, peer_host = self.socket.accept()

        if self.new_connection_callback and conn_socket is not None and peer_host is not None:
            self.new_connection_callback(conn_socket, peer_host)
