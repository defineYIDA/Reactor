# encoding=utf8


class Codec(object):

    def encode(self, msg):
        """
        自定义协议的编码
        """
        raise NotImplementedError

    def decode(self, data):
        """
        自定义协议的解码
        """
        raise NotImplementedError


# packet 协议的编解码器
from packet_codec import PacketCodec
# msg 协议的编解码器
from msg_codec import MsgCodec

Protocol_Codec = MsgCodec
