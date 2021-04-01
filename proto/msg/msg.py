# encoding=utf8
from src.proto.protocol import Protocol

class Msg(Protocol):
    """msg协议"""

    MAGIC_NUMBER = 0x12345678  # 魔数，用来做报文校验
    MAGIC_NUMBER_LEN = 4       # 魔数长度(4字节)
    PROTOCOL_VERSION = 2       # 协议版本

    DATA_FIELD_OFFSET = 12     # 数据域长度字段的偏移
    DATA_FIELD_LENGTH = 4      # 数据域长度字段的长度

    def __init__(self, command, data=None):
        self.data = data if data else {}
        self.command = command

    @property
    def version(self):
        return PROTOCOL_VERSION

    def get_command(self):
        return self.command
