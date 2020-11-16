# encoding=utf8

import cPickle
import struct
from codec import Codec
from protocol import Protocol


class PacketCodec(Codec, Protocol):
    """
    自定义协议编解码器
    编解码方式：序列化
    """

    BYTES_ORDER = '!'  # 网络字节序

    def __init__(self):

        self._packet_type_map = []  # 协议消息包的映射

        self._serializer_map = []  # 序列化方式的映射

        # header ， 魔数 + 协议版本 + 指令 + 数据长度
        self._header_fmt = self.BYTES_ORDER + '4I'  # 报文头部的fmt

        self._header_len = struct.calcsize(self._header_fmt)  # 报文头部长度

    @property
    def version(self):
        return 1

    def encode(self, packet):
        """
        自定义 packet 协议的编码
        +--------+----------+-------+--------+------------------+
        | 魔数   | 协议版本  |  指令 | 数据长度 |     数据         |
        +-------+----------+-------+--------+------------------+
         4byte     4byte    4byte    4byte       N byte
        """
        serialize_data = cPickle.dumps(packet)  # 序列化报文

        data = struct.pack(self._header_fmt, Protocol.MAGIC_NUMBER,
                           self.version,
                           packet.get_command(),
                           len(serialize_data))

        return data + serialize_data

    def decode(self, buffer):
        if not buffer or buffer.size < self._header_len:
            # 未接收到一个完整的包（防止出现粘包半包）
            return None, None

        (magic, ver, command, data_len) = struct.unpack(self._header_fmt, buffer.read(self._header_len))

        # print (magic, ver, command, data_len)

        if magic != Protocol.MAGIC_NUMBER:
            raise Exception("不支持当前客户端使用的消息协议")

        # version 提供可扩展性，后续添加其他的协议版本

        if ver != self.version:
            raise Exception("当前客户端使用的消息协议和服务端不统一")

        if buffer.size - self._header_len < data_len:
            # 未接收到一个完整的包（防止出现粘包半包）
            return None, None

        buffer.add_read_index(self._header_len)

        packet = cPickle.loads(buffer.read(data_len))  # TODO 根据command，反序列化得到对应packet
        # print packet.get_command()

        buffer.add_read_index(data_len)  # 更改read指针

        return command, packet


def _test(b, en):
    import time
    time.sleep(1)
    i = 0
    while i < len(en):
        if i + 20 < len(en):
            b.append(en[i:i + 20])
        else:
            b.append(en[i:])


if __name__ == '__main__':
    import message_packet, buffer, thread
    msg = message_packet.MessagePacket("hello!!!")
    codec = PacketCodec()
    en = codec.encode(msg)
    b = buffer.Buffer()
    b.append(en)
    # 模拟粘包
    msg1 = message_packet.MessagePacket("hello!!!")
    en1 = codec.encode(msg)
    b.append(en1[:10])
    codec.decode(b)
    b.append(en1[10:])
    codec.decode(b)

    print "----------------粘包模拟-------------------------"
    b.reset()
    b.append('')  # 模拟包未接收完
    # thread.start_new_thread(_test, (b, en))
    en = en + en
    i = 0
    while i <= len(en):
        command, packet = codec.decode(b)
        if not packet:
            print "没用一个完整的包"
        else:
            print command, packet.get_command()

        if i + 50 < len(en):
            b.append(en[i:i + 50])
            i += 50
        elif i == len(en):
            break
        else:
            b.append(en[i:])
            i = len(en)