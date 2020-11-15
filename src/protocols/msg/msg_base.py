# encoding=utf8

from msg import Msg


class MsgBase(Msg):
    """
    解码事用来初始化Msg协议包
    """

    def __init__(self, command, data):
        if not data:
            self.data = {}
        else:
            self.data = data
        self.command = command

    def get_command(self):
        return self.command
