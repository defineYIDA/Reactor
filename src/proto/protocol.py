# encoding=utf8


class Protocol(object):

    @property
    def version(self):
        """
        协议的版本类型，决定编解码方式
        """
        raise NotImplementedError

