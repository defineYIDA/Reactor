# encoding=utf8
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class Buffer(object):

    def __init__(self, max_size=65535):
        self._buf = StringIO()
        self.read_index = 0
        self.write_index = 0
        self._max_size = max_size

    @property
    def size(self):
        return self.write_index - self.read_index

    def reset(self):
        del self._buf
        self._buf = StringIO()
        self.read_index = 0
        self.write_index = 0

    def append(self, data):
        if not data or len(data) == 0:
            return

        # 文件指针移到末尾
        # 每一次read前都需要seek
        # 0: absolute; 1: relative; 2: relative to EOF
        self._buf.seek(0, 2)
        self._buf.write(data)
        # 标识写指针
        self.write_index += len(data)

    def read(self, size, s_index=0):
        """
        读取数据
        :param size: 读取长度
        :param s_index: 读取的起始位置，相对于read_index
        :return:
        """
        assert size >= 0 and self.read_index <= self.write_index
        assert 0 <= s_index <= self.write_index - self.read_index

        real_size = min(size, self.write_index - s_index)
        if real_size == 0:
            return ''

        # 起始位置为相对于read_index偏移s_index的位置
        self._buf.seek(self.read_index + s_index)
        buf = self._buf.read(real_size)
        self._buf.seek(self.read_index)
        return buf

    def get_all(self):
        """
        一次性将缓冲区数据全部发送
        """
        self._buf.seek(self.read_index)
        return self._buf.read()

    def add_read_index(self, count):
        """
        改变read_index，在read的时候恢复read指针，在这里统一改变
        解决消息粘包到达时的丢失
        """
        self.read_index += count
        if self.read_index > self.write_index:
            self.read_index = self.write_index
        if self.read_index == self.write_index and self.write_index > self._max_size:
            self.reset()
