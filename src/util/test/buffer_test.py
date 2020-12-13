# encoding=utf8
from cStringIO import StringIO

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
