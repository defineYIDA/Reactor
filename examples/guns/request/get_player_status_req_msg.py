# encoding=utf8

from msg import Msg
from command import Command


class GetPlayerStatusReqMsg(Msg):
    """
    获得玩家状态请求

    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.GET_PLAYER_STATUS_REQUEST
