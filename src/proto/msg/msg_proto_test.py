# encoding=utf8
from src.proto.msg.msg import Msg


class GetSettingReqMsg(Msg):

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return 1


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
    from src.util.buffer import Buffer
    from src.proto.msg.msg_codec import MsgCodec

    msg = GetSettingReqMsg({
        "data": [1, 2, 3],
    })
    codec = MsgCodec()
    s = codec.encode(msg)
    # print s[12:16]

    b = Buffer()
    b.append(s)

    import struct
    import json
    print len(json.dumps(msg.data))

    b._buf.seek(12, 0)
    data_len = struct.unpack('!I', b._buf.read(4))
    print data_len


    command, login = codec.decode(b)

    print command
    print str(login.data)
