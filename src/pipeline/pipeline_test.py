# encoding=utf8
from pipeline import Pipeline
from src.proto.msg.msg_handler import MsgInboundHandler, MsgOutboundHandler


class MsgDecodeHandler(MsgInboundHandler):

    def __init__(self):
        super(MsgDecodeHandler, self).__init__()

    def handle_read(self, ctx, msg):
        print("decode ..." + msg['data'])
        msg['data'] += ' -1'
        self.handle_next(ctx, msg)


class MsgEncodeHandler(MsgOutboundHandler):

    def __init__(self):
        super(MsgEncodeHandler, self).__init__()

    def handle_read(self, ctx, msg):
        print("encode ..." + msg['data'])
        msg['data'] += ' -2'
        self.handle_next(ctx, msg)


class MsgInboundHandler1(MsgInboundHandler):

    def __init__(self):
        super(MsgInboundHandler1, self).__init__(1)

    def handle_read(self, ctx, msg):
        print('MsgInboundHandler1 ...' + msg['data'])
        msg['data'] += ' -3'
        self.handle_next(ctx, msg)


class MsgInboundHandler2(MsgInboundHandler):

    def __init__(self):
        super(MsgInboundHandler2, self).__init__(1)

    def handle_read(self, ctx, msg):
        print('MsgInboundHandler2 ...' + msg['data'])
        msg['data'] += ' -4'
        self.handle_next(ctx, msg)


class MsgOutboundHandler1(MsgOutboundHandler):

    def __init__(self):
        super(MsgOutboundHandler1, self).__init__(2)

    def handle_read(self, ctx, msg):
        print('MsgOutboundHandler1 ...' + msg['data'])
        msg['data'] += ' -5'
        self.handle_next(ctx, msg)


if __name__ == '__main__':
    from channel_context import ChannelContext

    pipeline = Pipeline()
    channel_ctx = ChannelContext(11, pipeline)

    pipeline.add_last(MsgDecodeHandler())
    pipeline.add_last(MsgEncodeHandler())
    handler1 = MsgInboundHandler1()
    pipeline.add_last(handler1)
    pipeline.add_last(MsgInboundHandler2())
    pipeline.add_last(MsgOutboundHandler1())

    msg1 = {'command': 1, 'data': 'msg1'}
    msg2 = {'command': 2, 'data': 'msg2'}

    pipeline.inbound_process(channel_ctx, msg1)
    # print '-------------------------------------'
    # msg3 = {'command': 1, 'data': 'msg1'}
    # pipeline.remove(handler1)
    # pipeline.inbound_process(channel_ctx, msg3)
    # print '-------------------------------------'
    # msg4 = {'command': 1, 'data': 'msg1'}
    # pipeline.add_last(handler1)
    # pipeline.inbound_process(channel_ctx, msg4)

    # print '-------------------------------------'
    # print hash(MsgDecodeHandler())
    # print hash(MsgInboundHandler1())
