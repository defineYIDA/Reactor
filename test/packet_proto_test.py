# encoding=utf8
import sys,os
sys.path.append(os.path.realpath('.'))
from src.util.buffer import Buffer
from proto.packet.packet_codec import PacketCodec
from proto.packet.message_packet import MessagePacket


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
    msg = MessagePacket("hello!!!")
    codec = PacketCodec()
    en = codec.encode(msg)
    b = Buffer()
    b.append(en)
    # 模拟粘包
    msg1 = MessagePacket("hello!!!")
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
