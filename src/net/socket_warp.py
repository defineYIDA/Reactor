# encoding=utf8

import socket
from src.util import error


class Socket(object):
    """
    socket的包装
    """

    def __init__(self, conn_socket=None):
        if conn_socket:
            self.sock = conn_socket
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 地址复用,解决因为tcp time_wait 导致的服务器监听无法快速重启
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # TCP keep alive 保活
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)  # 关闭tcp nagle 机制,提高实时性

        self.sock.setblocking(False)  # 非阻塞

    @property
    def fd(self):
        return self.sock.fileno()

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except socket.error as e:
            if e.args[0] in (error.ENOTCONN, error.EBADF):
                # error.ENOTCONN: 关闭一个已经被关闭了的连接
                # error.EBADF: 描述符失效
                return
            else:
                LOG.error('socket close error')


class ServerSocket(Socket):
    """
    server socket
    """

    def bind_and_listen(self, host_addr, backlog=socket.SOMAXCONN):
        self.sock.bind(host_addr)
        self.sock.listen(backlog)  # set backlog 最终值由该参数和系统共同决定
        LOG.info("Listen:" + str(host_addr) + "successful !")

    def accept(self):
        """
        server socket accept (listen socket)
        """
        conn_socket = None
        peer_host = None

        try:
            conn_socket, peer_host = self.sock.accept()
            return conn_socket, peer_host
        except socket.error as e:
            if e.args[0] in error.SHOULDCONTINUE:
                return None, None
            elif e.args[0] == error.ECONNABORTED:
                # ECONNABORTED : 客户端发送了rst
                return None, None
            else:
                LOG.error('socket accept error')
                raise


class ClientSocket(Socket):
    """
    client socket
    """

    def connect(self, dist_address):
        """
        conn to server
        """
        import os
        from connector import ConnectorState

        ret = self.sock.connect_ex(dist_address)

        if ret in error.CONNECTING:
            # 正在建立连接
            return ConnectorState.CONNECTING
        elif ret == error.EINTR and os.name in ('nt', 'ce'):
            # 正在建立连接
            return ConnectorState.CONNECTING
        elif ret in (0, error.EISCONN):
            return ConnectorState.CONNECTED
        else:
            LOG.error('socket connect error')
            return ConnectorState.ERROR

    def send(self, data):
        """
        返回以发送的长度，和是否关闭连接
        """
        is_close = False
        try:
            sent_count = self.sock.send(data)
            return sent_count, is_close

        except socket.error as e:
            if e.args[0] in error.SHOULDCONTINUE:
                return 0, is_close
            elif e.args[0] in error.DISCONNECTED:
                is_close = True
                return 0, is_close
            else:
                LOG.error('socket send failed')
                raise

    def recv(self, buffer_size):
        is_close = False
        try:
            recv_data = self.sock.recv(buffer_size)
            if recv_data:
                return recv_data, is_close
            else:
                is_close = True
                return '', is_close
        except socket.error as e:
            if e.args[0] in error.SHOULDCONTINUE:
                return '', is_close
            elif e.args[0] in error.DISCONNECTED:
                is_close = True
                return '', is_close
            else:
                LOG.error('socket recv failed')
                raise

    def get_peer_name(self):
        """
        获得对端的host，判断连接是否建立成功
        """
        is_success = True
        try:
            return self.sock.getpeername(), is_success
        except:
            is_success = False
            return None, is_success
