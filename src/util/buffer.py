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

    def read(self, size):
        assert size >= 0 and self.read_index <= self.write_index

        real_size = min(size, self.write_index - self.read_index)
        if real_size == 0:
            return ''

        self._buf.seek(self.read_index, 0)
        buff = self._buf.read(real_size)
        self._buf.seek(self.read_index, 0)  # 恢复

        return buff

    def get_all(self):
        """
        一次性将缓冲区数据全部发送
        """
        self._buf.seek(self.read_index, 0)
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


if __name__ == '__main__':
    buffer = StringIO()
    buffer.write("12345678910")
    print buffer.tell()
    print buffer.read()
    print buffer.getvalue()
    print buffer.tell()
    print '*' * 20
    buffer.seek(0)
    print buffer.tell()
    print buffer.read()
    print buffer.tell()
    print '*' * 20
    buffer.seek(0)
    print buffer.read(4)
    print buffer.tell()
    buffer.seek(6)
    buffer.truncate()  # 无参从读写位置起切断数据，参数size开始裁剪的位置，裁剪完后读写位置改变
    print buffer.tell()
    print buffer.read()
    print buffer.getvalue()
