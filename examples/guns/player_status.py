# encoding=utf8
from db_manager import dbManager
from setting import PlayerSetting
from setting import EnemySetting

class PlayerStatus(object):
    """
    玩家状态，在登陆时初始化，存放从服务端获取到的玩家状态
    """

    def __init__(self):
        self.player_setting = PlayerSetting()
        self.enemy_setting = EnemySetting()

    def insert_player_status(self, key, id):
        return dbManager.insert_player_status(key, id, self.player_setting.get('hp'), self.player_setting.get('magazine_amout'),
                                              self.player_setting.get('total_bullet'))

    def get_player_status(self, key, id):
        return dbManager.select_player_status(key, id)

    def damage(self, key, id):
        """
        玩家被攻击，hp-敌人伤害值
        """
        row = dbManager.select_player_status(key, id)
        if row:
            dbManager.update_player_status(key, id, row[2] - self.enemy_setting.get("damage"), row[3], row[4])
            print 'HP--'
            return True
        else:
            return False

    def shoot(self, key, id):
        """
        玩家开枪，子弹--
        """
        row = dbManager.select_player_status(key, id)
        if row:
            if row[3] > 0:
                bullet = row[3] - 1
                dbManager.update_player_status(key, id, row[2], bullet, row[4])
                print 'bullet--'
                return True
            else:
                return False
        else:
            return False

    def reload(self, key, id):
        """
        玩家换弹，弹夹子弹和子弹总数更改
        """
        row = dbManager.select_player_status(key, id)
        if row:
            temp = self.player_setting.get('magazine_amout') - row[3]  # 需要填充的子弹数
            if temp <= row[4]:
                bullet = self.player_setting.get('magazine_amout')
                total_bullet = row[4] - temp
                dbManager.update_player_status(key, id, row[2], bullet, total_bullet)
            else:
                bullet = row[3] + row[4]
                total_bullet = 0
                dbManager.update_player_status(key, id, row[2], bullet, total_bullet)
            return True
        else:
            return False


PlayerStatus = PlayerStatus()
