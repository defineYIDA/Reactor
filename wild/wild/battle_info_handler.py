# encoding=utf8
import time
import json
from room_manager import room_manager
from battle_info_res_msg import BattleInfoResMsg
from conf import Conf


class BattleInfoHandler(object):
    """"
    战斗消息处理
    """

    def __init__(self):
        pass

    def battle_info_handler(self, tcp_connection, msg):
        """
        分发给房间其它人
        :param tcp_connection:
        :param msg:
        :return:
        """
        res_msg = BattleInfoResMsg(msg.data)
        if res_msg.data['type'] == Conf.BATTLE_REQ:
            room_manager.send_msg_to_room_other_player(msg.data['id'], msg.data['room_id'], res_msg)
        elif res_msg.data['type'] == Conf.DEATH_REQ:
            from game_logic import GameLogic
            rank = room_manager.count_rank(msg.data['id'], msg.data['room_id'])
            res_msg.data['rank'] = rank
            res_msg.data['gold'] = GameLogic().calculate_gold(rank, len(room_manager.room_map[msg.data['room_id']]))
            print str(res_msg.data)
            room_manager.send_room_msg(msg.data['room_id'], res_msg)
