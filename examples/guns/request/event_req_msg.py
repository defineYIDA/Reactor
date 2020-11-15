# encoding=utf8

from msg import Msg
from command import Command


class EventReqMsg(Msg):
    """
    玩家事件请求
    type：0-被攻击；1-开枪；2-换弹
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.EVENT_REQUEST
