# encoding=utf8

from msg import Msg
from command import Command


class EventResMsg(Msg):
    """
    玩家状态响应
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.EVENT_RESPONSE
