# encoding=utf8


class PlayerSetting(object):
    """
    玩家核心参数
    """
    def __init__(self):
        self.dict = {
            'hp': 10,  # 玩家血量
            'speed': 5,  # 移动速度
            'damage': 1,  # 伤害值
            'magazine_amout': 10,  # 弹夹容量
            'total_bullet': 50,  # 子弹数
        }

    def get(self, key):
        return self.dict[key]


class EnemySetting(object):
    """
    敌人核心参数
    """
    def __init__(self):
        self.dict = {
            'hp': 5,  # 敌人血量
            'speed': 5,  # 移动速度
            'damage': 1,  # 伤害值
            'shoot_rate': 10,  # 攻击间隔
        }

    def get(self, key):
        return self.dict[key]