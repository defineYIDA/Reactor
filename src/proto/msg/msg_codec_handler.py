# encoding=utf8
from src.proto.msg.msg_codec import MsgCodec
from src.pipeline.pipeline_handler import InboundHandler, OutboundHandler

class MsgDecodeHandler(InboundHandler):

    def __init__(self):
        super(MsgDecodeHandler, self).__init__()

    def handle_read(self, ctx, buff):
        codec = MsgCodec()
        command, msg = codec.decode(buff)
        if command is None or msg is None:
            return
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