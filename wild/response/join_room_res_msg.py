# encoding=utf8

from msg import Msg
from command import Command


class JoinRoomResMsg(Msg):
    """
    加入房间响应报文
    data:
    {
      "room_id": "",
      "status": "",
      "msg": "", 所有玩家的列表
    }
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.JOIN_ROOM_RESPONSE
