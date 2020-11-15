# encoding=utf8

from msg import Msg
from command import Command


class JoinRoomReqMsg(Msg):
    """
    加入房间请求报文
    data:
    {
      "id": "",
    }
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.JOIN_ROOM_REQUEST

