# encoding=utf8


class Codec(object):

    def encode(self, msg):
        """自定义协议的编码"""
        raise NotImplementedError

    def decode(self, data):
        """自定义协议的解码"""
        raise NotImplementedError
