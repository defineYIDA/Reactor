from src.proto.msg.msg import Msg
from src.proto.msg.command import Command


class BattleInfoResMsg(Msg):
    """
    data:
    {
      "id": "",
      "room_id": "",
      "maxhp": "",
      "hp": "",
      "mp": "",
      "energy": "",
      "death": "",
    }
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.BATTLE_INFO_RESPONSE
