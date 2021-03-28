# encoding=utf8
from src.tcp.tcp_client import TcpClient
from src.proto.msg.msg import Msg
from src.proto.msg.msg_handler import MsgInboundHandler


class TestClient(TcpClient):

    HEART_BEAT_INTERNAL = 5  # 心跳间隔

    def init_pipeline(self, pipe):
        from src.proto.msg.msg_codec_handler import MsgEncodeHandler, MsgDecodeHandler
        from src.proto.msg.msg_heart_beat_handler import MsgHeartBeatHandler
        pipe.add_last(MsgDecodeHandler())
        pipe.add_last(EchoHandler())
        pipe.add_last(MsgHeartBeatHandler())
        pipe.add_last(MsgEncodeHandler())

    def on_connection_ready(self, conn):
        import functools
        from src.util.timer import Timer
        from src.proto.msg.heart_beat_msg import HeartBeatMsg
        self.add_timer(Timer(TestClient.HEART_BEAT_INTERNAL, functools.partial(conn.ctx.direct_send, HeartBeatMsg())))

    def send_msg(self, data):
        from src.proto.msg.msg_codec import MsgCodec
        try:
            encode = MsgCodec()
            data = encode.encode(data)
        except Exception, e:
            LOG.error(e.message)
            return
        self.send(data)

class EchoHandler(MsgInboundHandler):

    def __init__(self):
        super(EchoHandler, self).__init__(1)

    def handle_read(self, ctx, msg):
        print(msg.data)

class ReqMsg(Msg):

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return 1

def send(tcp_client):
    import time
    time.sleep(2)
    msg = ReqMsg({
        "data": [1, 2, 3],
    })
    tcp_client.send_msg(msg)

if __name__ == '__main__':
    import thread
    client = TestClient(10)
    client.connect(('127.0.0.1', 8080))
    thread.start_new_thread(send, (client,))
    client.run()
