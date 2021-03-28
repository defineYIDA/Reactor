#encoding=utf8
from proto.msg.msg_handler import MsgInboundHandler

class MsgHeartBeatHandler(MsgInboundHandler):

    def __init__(self):
        super(MsgHeartBeatHandler, self).__init__(0)

    def handle_read(self, ctx, msg):
        import time
        ctx.conn().last_recv_heart_time = time.time()
        print('recv heartbeat {}'.format(int(time.time())))