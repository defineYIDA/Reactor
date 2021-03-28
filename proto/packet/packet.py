# encoding=utf8


class Packet(object):
    """
    消息包协议
    """

    def get_command(self):
        raise NotImplementedError
