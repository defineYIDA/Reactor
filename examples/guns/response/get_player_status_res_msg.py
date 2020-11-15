# encoding=utf8

from msg import Msg
from command import Command


class GetPlayerStatusResMsg(Msg):
    """
    获得玩家状态响应
    """

    def __init__(self, data):
        if data:
            self.data = {
                'status': 'true',
                'game_key': data[0],
                'id': data[1],
                'hp': data[2],
                'bullet_amount': data[3],
                'total_bullet': data[4]
            }
        else:
            self.data = {
                'status': 'false'
            }


    def get_command(self):
        return Command.GET_PLAYER_STATUS_RESPONSE
