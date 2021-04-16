#encoding=utf8
from proto.msg.msg import Msg
from src.tcp.tcp_server import TcpServer
from proto.msg.msg_handler import MsgInboundHandler

class ServerTest(TcpServer):

    def __init__(self):
        super(ServerTest, self).__init__(('', 8080), time_out=1)

    def init_pipeline(self, pipe):
        from proto.msg.msg_splitter import MsgSplitter
        pipe.add_last(MsgSplitter())
        from proto.msg.msg_codec_handler import MsgEncodeHandler, MsgDecodeHandler
        pipe.add_last(MsgDecodeHandler())
        pipe.add_last(EchoHandler())
        from proto.msg.msg_heart_beat_handler import MsgHeartBeatHandler
        pipe.add_last(MsgHeartBeatHandler())
        pipe.add_last(MsgEncodeHandler())
        from proto.msg.msg_codec import MsgCodec
        pipe.set_proto_codec(MsgCodec())

    def send_heartbeat(self, conn):
        from proto.msg.heart_beat_msg import HeartBeatMsg
        conn.ctx.direct_send(HeartBeatMsg())


class EchoHandler(MsgInboundHandler):

    def __init__(self):
        super(EchoHandler, self).__init__(1)

    def handle_read(self, ctx, msg):
        print(msg.data)
        msg = ResMsg({
        "data": [11, 22, 33],
        })
        ctx.write_and_flush(msg)

class ResMsg(Msg):

    def __init__(self, data):
        super(ResMsg, self).__init__(1, data)


if __name__ == '__main__':
    server_ins = ServerTest()
    server_ins.heart_beat()
    server_ins.run()