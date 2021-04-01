# encoding=utf8
from proto.msg.msg import Msg


class ReqMsg(Msg):

    def __init__(self, data):
        super(ReqMsg, self).__init__(1, data)


def run_test():
    import struct
    import json
    from src.util.buffer import Buffer
    from proto.msg.msg_codec import MsgCodec

    msg = ReqMsg({
        "data": [1, 2, 3],
    })
    codec = MsgCodec()
    s = codec.encode(msg)
    # print s[12:16]

    b = Buffer()
    # 随意填充buffer
    dirty = struct.pack('!I', 1111)
    dirty_len = len(dirty)
    b.append(dirty)
    b.read(dirty_len)
    b.add_read_index(dirty_len)
    print 'read_index = ' + str(b.read_index)

    b.append(s)
    print 'data_len = ' + str(len(json.dumps(msg.data)))

    # 移动到协议首部长度域的位置
    # idx = b.read_index
    # b.add_read_index(12)
    # data = struct.unpack('!I', b.read(4))
    data = struct.unpack('!I', b.read(4, 12))
    print 'data_len = ' + str(data)
    print 'read_index = ' + str(b.read_index)

    # 恢复初始位置
    # b.read_index = idx

    command, msg = codec.decode(b)
    print str(command) + '--' + str(msg.data)
    print 'read_index = ' + str(b.read_index)
