# encoding=utf8


class HandlerBase(object):

    def __init__(self):
        self._ctx_ref = None  # weak_ref

    def handle_read(self, ctx, msg):
        raise NotImplementedError

    def verify(self, ctx, msg):
        """校验handler是否需要处理这个msg"""
        raise NotImplementedError

    def bind_ctx(self, ctx):
        import weakref
        self._ctx_ref = weakref.ref(ctx)

    def handle_next(self, ctx, msg):
        if self._ctx_ref:
            self._ctx_ref().handle_next(ctx, msg)
        else:
            raise Exception('handler no bind context')

    def __hash__(self):
        return hash(type(self).__name__)


class InboundHandler(HandlerBase):
    """入站事件"""

    def __init__(self):
        super(InboundHandler, self).__init__()

    def handle_read(self, ctx, msg):
        self.handle_next(ctx, msg)

    def verify(self, ctx, msg):
        return False


class OutboundHandler(HandlerBase):
    """出站事件"""

    def __init__(self):
        super(OutboundHandler, self).__init__()

    def handle_read(self, ctx, msg):
        self.handle_next(ctx, msg)

    def verify(self, ctx, msg):
        return False
