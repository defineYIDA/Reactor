# encoding=utf8

from msg import Msg


class HeartBeatMsg(Msg):
    """
    心跳消息
    """
    def __init__(self):
        self.data = {}

    def get_command(self):
        return 0
