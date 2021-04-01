# encoding=utf8
from src.pipeline.pipeline_handler import Splitter


class LengthFieldSplitter(Splitter):

    def __init__(self, field_offset, field_length):
        """
        基于长度字段的协议拆包器
        :param field_offset: 字段在协议中的偏移
        :param field_length: 字段长度
        """
        super(LengthFieldSplitter, self).__init__()
        if field_offset < 0 or field_length < 0:
            raise Exception('Splitter init failed, parameter error !')

        self._field_offset = field_offset
        self._field_length = field_length

        self._magic_fmt = '!I'
        self._field_fmt = '!I'

    def check(self, msg_buffer):
        # check protocol available
        return True

    def handle_read(self, ctx, msg_buffer):
        """
        校验是否到达一个完整协议包体
        :param ctx:
        :param msg_buffer:
        :return: bool
        """
        import struct

        if not self.check(ctx, msg_buffer):
            return False

        buf_size = msg_buffer.size
        if buf_size < self._field_offset + self._field_length:
            return False

        # 校验数据域数据是否完整
        (field_val,) = struct.unpack(self._field_fmt, msg_buffer.read(self._field_length, self._field_offset))
        if msg_buffer.size - self._field_offset - self._field_length < field_val:
            return False
        return True

    def verify(self, ctx, msg):
        return True
