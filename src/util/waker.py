# encoding=utf8


class Waker(object):
    """
    唤醒阻塞的poller（阻塞的IO复用函数）
    """

    def wake_up(self):
        raise NotImplementedError

    def handle_read(self):
        # 如果处于LE水平触发，应该对socket的可读事件进行处理，
        # 不然会导致该socket一直处于就绪状态出现空轮询
        raise NotImplementedError


class SocketWaker(Waker):
    """
    using a pair of sockets rather than pipes
    """

    def __init__(self, loop):
        import socket, channel
        self._loop = loop
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        server.bind(('127.0.0.1', 0))
        server.listen(1)
        client.connect(server.getsockname())
        reader, addr = server.accept()
        client.setblocking(False)
        reader.setblocking(False)
        self.r = reader
        self.w = client
        self.socket_channel = channel.Channel(loop, self.r.fileno())  # 监听该socket
        self.socket_channel.need_read = True
        self.socket_channel.set_read_callback(self.handle_read)
        self.socket_channel.add_loop()

    def wake_up(self):
        """
        Send a byte to my connection.
        """
        self.w.send('p')
        print 'wake_up'

    def handle_read(self):
        self.r.recv(1)


class PipeWaker(Waker):
    """
    self-pipe trick
    """

    def __init__(self, loop):
        import os, channel
        self._loop = loop
        self.rfd, self.wfd = os.pipe()
        # 监听pipe，win不支持 https://github.com/defineYIDA/Reactor/issues/1
        self.pipe_channel = channel.Channel(self._loop, self.rfd)

        self.chr = 'p'
        # 注册读事件
        self.pipe_channel.read_callback = self.handle_read
        self.pipe_channel.need_read = True

    def wake_up(self):
        # 向管道中写入一个字节
        import os
        os.write(self.wfd, self.chr)

    def handle_read(self):
        # 被channel 回调
        import os
        recv_chr = os.read(self.rfd, 1)
        if not recv_chr == self.chr:
            pass


import platform

waker = None
if platform.system() == 'Windows':
    waker = SocketWaker
else:
    waker = PipeWaker
