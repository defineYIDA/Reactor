# encoding=utf8
from src.proto.protocol import Protocol

class Packet(Protocol):
    """消息包协议"""
    MAGIC_NUMBER = 0x12345678  # 魔数，用来做报文校验
    MAGIC_NUMBER_LEN = 4       # 魔数长度(4字节)
    PROTOCOL_VERSION = 1       # 协议版本

    @property
    def version(self):
        return PROTOCOL_VERSION
