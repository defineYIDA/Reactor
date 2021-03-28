# encoding=utf8
from src.pipeline.handler_context import HandlerContext
from src.pipeline.pipeline_handler import InboundHandler, OutboundHandler, Splitter


class Pipeline(object):

    def __init__(self):
        """责任链"""
        self._inbound_head = HandlerContext(InboundHandler())  # 入站链表
        self._outbound_head = HandlerContext(OutboundHandler())  # 出站链表

        self.splitter = None  # 协议拆包器
        self.codec = None  # 编解码器

        self._inbound_tail = self._inbound_head
        self._outbound_tail = self._outbound_head

        self._handler_dict = {}  # {hash(handler), handler_ctx}

    def add_last(self, handler):
        if not handler:
            return
        # 判断重复添加，防止出现环状链表
        if self._handler_dict.has_key(hash(handler)):
            raise Exception("pipeline add handler repeat")

        if isinstance(handler, InboundHandler):
            in_ctx = HandlerContext(handler)
            self._inbound_tail.next = in_ctx
            in_ctx.prev = self._inbound_tail
            self._inbound_tail = in_ctx
            self._handler_dict[hash(handler)] = in_ctx
            return in_ctx

        elif isinstance(handler, OutboundHandler):
            out_ctx = HandlerContext(handler)
            self._outbound_tail.next = out_ctx
            out_ctx.prev = self._outbound_tail
            self._outbound_tail = out_ctx
            self._handler_dict[hash(handler)] = out_ctx
            return out_ctx

        elif isinstance(handler, Splitter):
            self.splitter = handler
            return handler
        else:
            raise Exception("pipeline add handler type error")

    def inbound_process(self, ctx, msg):
        """请求入站处理"""
        if self._inbound_head:
            self._inbound_head.handle(ctx, msg)

    def outbound_process(self, ctx, msg):
        """请求出战处理"""
        if self._outbound_head:
            self._outbound_head.handle(ctx, msg)

    def inbound_end(self, ctx, msg):
        """入站事件结束"""
        # if self._outbound_head:
        #     self.outbound_process(ctx, msg)
        # else:
        #     self.outbound_end(ctx, msg)
        pass

    def outbound_end(self, ctx, msg):
        """出站结束"""
        ctx.conn().send(msg)
        # LOG.info('outbound end')

    def remove(self, handler):
        """移除handler"""
        ctx = self._handler_dict.get(hash(handler), None)
        if ctx:
            if not ctx.prev:
                # 头节点是临时节点不能删除
                return
            ctx.prev.next = ctx.next
            del self._handler_dict[hash(handler)]

    def set_proto_codec(self, codec):
        """"设置协议编解码器"""
        from proto.codec import Codec
        if not isinstance(codec, Codec):
            return
        self.codec = codec
