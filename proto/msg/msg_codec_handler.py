# encoding=utf8
from proto.msg.msg import Msg
from proto.msg.msg_codec import MsgCodec
from src.pipeline.pipeline_handler import InboundHandler, OutboundHandler

class MsgDecodeHandler(InboundHandler):

    def __init__(self):
        super(MsgDecodeHandler, self).__init__()

    def handle_read(self, ctx, buff):
        # 协议包入口，解码时会校验是否符合协议定义，关闭非法协议的连接
        try:
            codec = MsgCodec()
            command, msg = codec.decode(buff)
            if command is None or msg is None:
                return
        except Exception, e:
            ctx.conn().handle_close()
            LOG.error('Connection close! received illegal protocol. ' + e.message)
        self.handle_next(ctx, msg)

    def verify(self, ctx, msg):
        return True


class MsgEncodeHandler(OutboundHandler):

    def __init__(self):
        super(MsgEncodeHandler, self).__init__()

    def handle_read(self, ctx, buff):
        codec = MsgCodec()
        data = codec.encode(buff)
        if data:
            self.handle_next(ctx, data)

    def verify(self, ctx, msg):
        return True