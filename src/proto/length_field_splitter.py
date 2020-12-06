# encoding=utf8
from src.pipeline.pipeline_handler import InboundHandler


class LengthFieldSplitter(InboundHandler):

    def __init__(self, field_offset, field_length):
        """
        基于长度字段的协议拆包器
        :param field_offset: 字段在协议中的偏移
        :param field_length: 字段长度
        """
        super(LengthFieldSplitter, self).__init__()
        self._field_offset = field_offset
        self._field_length = field_length

    def handle_read(self, ctx, msg_buffer):
        """
        校验是否到达一个完整协议包体
        :param ctx:
        :param msg_buffer:
        :return:
        """
        if not msg_buffer or msg_buffer.size < self._field_offset:
            return
        # TODO 得到字节流中某个位置的数据

    def verify(self, ctx, msg):
        return True
