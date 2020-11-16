# encoding=utf8


class Protocol(object):
    MAGIC_NUMBER = 0x12345678  # 魔数，用来做报文校验

    @property
    def version(self):
        """
        协议的版本类型，决定编解码方式
        """
        raise NotImplementedError

