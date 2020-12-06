# encoding=utf8


class HandlerContext(object):

    def __init__(self, handler):
        """handler在管道中的上下文"""
        handler.bind_ctx(self)
        self._handler = handler
        self.prev = None
        self.next = None

    def handle(self, ctx, msg):
        """执行当前handle"""
        if self._handler and self._handler.verify(ctx, msg):
            self._handler.handle_read(ctx, msg)
        else:
            self.handle_next(ctx, msg)

    def handle_next(self, ctx, msg):
        """调度到下一个handle"""
        from src.pipeline.pipeline_handler import InboundHandler, OutboundHandler

        if not ctx:
            raise Exception('channel context is none')

        if isinstance(self._handler, InboundHandler):
            if self.next:
                self.next.handle(ctx, msg)
            else:
                ctx.pipe.inbound_end(ctx, msg)
        elif isinstance(self._handler, OutboundHandler):
            if self.next:
                self.next.handle(ctx, msg)
            else:
                ctx.pipe.outbound_end(ctx, msg)