# encoding=utf8


class GameLogic(object):

    def __init__(self):
        pass

    def calculate_gold(self, rank, room_count):
        """
        简单计算一局游戏获得的金币
        :param rank:
        :param room_count:
        :return:
        """
        # 增加用户金币
        from db_manager import dbManager
        # dbManager.update_player_status()
        return (room_count - rank + 1) * 200