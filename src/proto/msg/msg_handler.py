# encoding=utf8
from src.pipeline.pipeline_handler import InboundHandler, OutboundHandler


class MsgInboundHandler(InboundHandler):

    def __init__(self, command=-1):
        super(MsgInboundHandler, self).__init__()
        """command == -1 代表所有协议包都要经过这个handler"""
        self.command = command

    def handle_read(self, ctx, msg):
        pass

    def verify(self, ctx, msg):
        if self.command == -1:
            return True
        else:
            return msg.get_command() == self.command


class MsgOutboundHandler(OutboundHandler):

    def __init__(self, command=-1):
        super(MsgOutboundHandler, self).__init__()
        self.command = command

    def handle_read(self, ctx, msg):
        pass

    def verify(self, ctx, msg):
        if self.command == -1:
            return True
        else:
            return msg.get_command() == self.command
