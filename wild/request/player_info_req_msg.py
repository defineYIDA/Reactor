# encoding=utf8

from msg import Msg
from command import Command


class PlayerInfoReqMsg(Msg):
    """
    登陆请求报文
    data:
    {
      "id": "",
      "room_id": "",
      "data": "",
      "type": "",
    }
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.PLAYER_INFO_REQUEST
