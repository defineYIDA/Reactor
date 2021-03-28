# encoding=utf8


class GameStatus(object):
    """
    游戏状态
    """

    def __init__(self, user_id, character, status):
        self.user_id = user_id
        self.character = character  # 角色
        self.status = status  # 游戏状态
        self.rank = -1  # -1代表未计算排名
