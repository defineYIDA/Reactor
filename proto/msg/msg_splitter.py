# encoding=utf8
from proto.msg.msg import Msg
from src.proto.length_field_splitter import LengthFieldSplitter

class MsgSplitter(LengthFieldSplitter):

    def __init__(self):
        super(MsgSplitter, self).__init__(Msg.DATA_FIELD_OFFSET, Msg.DATA_FIELD_LENGTH)

    def check(self, ctx, msg_buffer):
        import struct

        buf_size = msg_buffer.size
        if buf_size < Msg.MAGIC_NUMBER_LEN:
            # 这里不关闭连接
            return True

        # 校验magic_number
        (magic_number,) = struct.unpack(self._magic_fmt, msg_buffer.read(Msg.MAGIC_NUMBER_LEN))
        if magic_number != Msg.MAGIC_NUMBER:
            ctx.conn().handle_close()
            LOG.error('Connection close! received illegal protocol. magic number do not match')
            return False
        return True