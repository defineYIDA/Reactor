# encoding=utf8


class PlayerInfo(object):
    """
    玩家核心参数
    """
    def __init__(self, id='', character=''):
        self.dict = {
            'id': id,
            'hp': 5,
            'room_id': '',

            'px': 0,
            'py': 0,
            'pz': 0,

            'rx': 0,
            'ry': 0,
            'rz': 0,
            'rw': 0,

            'vertical': False,
            'horizontal': False,
            'sprint': False,
            'jump': False,
            'normalAttack': False,
            'comboAttack': False,
            'roll': False,

            'tx': 0,
            'ty': 0,
            'tz': 0,

            'character': character
        }

    def get(self, key):
        return self.dict[key]

    def set_pos(self, px, py, pz):
        self.dict['px'] = px
        self.dict['py'] = py
        self.dict['pz'] = pz

    def set_random_pos(self):
        """
        设置一个随机位置
        :return:
        """
        import random
        list_x = [-15, -10, 0, 10, 15]
        list_z = [5, -10]
        self.set_pos(random.choice(list_x), 0, random.choice(list_z))
