from msg import Msg
from command import Command


class BattleInfoReqMsg(Msg):
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
        return Command.BATTLE_INFO_REQUEST
