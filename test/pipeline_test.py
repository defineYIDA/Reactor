# encoding=utf8
from src.pipeline.pipeline import Pipeline
from src.pipeline.channel_context import ChannelContext
from src.proto.msg.msg_handler import MsgInboundHandler, MsgOutboundHandler
from src.proto.msg.msg import Msg


class TempObj(object):

    def send(self, *args, **kw):
        pass

class MsgDecodeHandler(MsgInboundHandler):

    def __init__(self):
        super(MsgDecodeHandler, self).__init__()

    def handle_read(self, ctx, msg):
        print("decode ..." + msg.data)
        msg.data += ' -1'
        self.handle_next(ctx, msg)


class MsgInboundHandler1(MsgInboundHandler):

    def __init__(self):
        super(MsgInboundHandler1, self).__init__(1)

    def handle_read(self, ctx, msg):
        print('MsgInboundHandler1 ...' + msg.data)
        msg.data += ' -3'
        self.handle_next(ctx, msg)


class MsgInboundHandler2(MsgInboundHandler):

    def __init__(self):
        super(MsgInboundHandler2, self).__init__(1)

    def handle_read(self, ctx, msg):
        print('MsgInboundHandler2 ...' + msg.data)
        msg.data += ' -4'
        self.handle_next(ctx, msg)


class MsgInboundHandler3(MsgInboundHandler):

    def __init__(self):
        super(MsgInboundHandler3, self).__init__(1)

    def handle_read(self, ctx, msg):
        print('MsgInboundHandler3 ...' + msg.data)
        new_msg = SimpleMsg(1, 'new msg')
        ctx.pipe.outbound_process(ctx, new_msg)


#############################################################################

class MsgEncodeHandler(MsgOutboundHandler):

    def __init__(self):
        super(MsgEncodeHandler, self).__init__()

    def handle_read(self, ctx, msg):
        print("encode ..." + msg.data)
        msg.data += ' -2'
        self.handle_next(ctx, msg)


class MsgOutboundHandler1(MsgOutboundHandler):

    def __init__(self):
        super(MsgOutboundHandler1, self).__init__(1)

    def handle_read(self, ctx, msg):
        print('MsgOutboundHandler1 ...' + msg.data)
        msg.data += ' -5'
        self.handle_next(ctx, msg)

class SimpleMsg(Msg):
    def __init__(self, command, data):
        self.command = command
        self.data = data
    
    def get_command(self):
        return self.command



def test1():
    """入站事件结束后，自动到出站事件（已改为主动调用出站事件）"""
    pipeline = Pipeline()
    temp = TempObj()
    channel_ctx = ChannelContext(temp, pipeline)

    pipeline.add_last(MsgDecodeHandler())
    pipeline.add_last(MsgEncodeHandler())
    handler1 = MsgInboundHandler1()
    pipeline.add_last(handler1)
    pipeline.add_last(MsgInboundHandler2())
    pipeline.add_last(MsgOutboundHandler1())

    msg1 = SimpleMsg(1, 'msg1')
    msg2 = SimpleMsg(2, 'msg2')

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


def test2():
    pipeline = Pipeline()
    temp = TempObj()
    channel_ctx = ChannelContext(temp, pipeline)

    pipeline.add_last(MsgDecodeHandler())
    pipeline.add_last(MsgEncodeHandler())
    pipeline.add_last(MsgInboundHandler1())
    pipeline.add_last(MsgInboundHandler2())
    pipeline.add_last(MsgOutboundHandler1())
    pipeline.add_last(MsgInboundHandler3())

    msg1 = SimpleMsg(1, 'msg1')
    res = pipeline.inbound_process(channel_ctx, msg1)
    print res

def run_test():
    # 测试大致流程
    test1()
    print '-------------------------------------'
    test2()