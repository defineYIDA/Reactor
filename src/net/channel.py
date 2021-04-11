# encoding=utf8


class Channel(object):
    """
    对socket的封装
    """

    def __init__(self, loop, fd):
        self._loop = loop
        self.fd = fd

        self.need_write = False
        self.need_read = False
        self.writable = False
        self.readable = False
        self.error = False

        self.is_accept = False  # is listen socket

        self.read_callback = None
        self.write_callback = None
        self.error_callback = None

    def add_loop(self):
        """
        添加到poll的map中进行轮询
        """
        self._loop.update_channel(self)

    def close(self):
        """
        移除当前channel从轮询器中
        """
        self._loop.remove_channel(self)
        # 防止内存泄漏
        self.read_callback = None
        self.write_callback = None
        self.error_callback = None

    def disable(self):
        """
        关闭对该channel的监测
        """
        self.need_write = False
        self.need_read = False
        self.is_accept = False

    def set_read_callback(self, method):
        self.read_callback = method

    def set_write_callback(self, method):
        self.write_callback = method

    def set_error_callback(self, method):
        self.error_callback = method

    def handle_event(self):
        """
        channel就绪执行回调
        """
        if self.readable and self.read_callback:
            self.read_callback()

        if self.writable and self.write_callback:
            self.write_callback()

        if self.error and self.error_callback:
            self.error_callback()
