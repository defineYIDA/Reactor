# encoding=utf8

import sqlite3


class DBManager(object):

    def __init__(self):
        self.conn = sqlite3.connect("guns.db")
        self.cur = self.conn.cursor()
        # 创建用户表
        self.cur.execute("CREATE TABLE IF NOT EXISTS user(id TEXT PRIMARY KEY,pwd TEXT)")
        # 创建用户状态表
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS playerstatus(game_key TEXT PRIMARY KEY,id TEXT,hp INTEGER,bullet_amount INTEGER,total_bullet INTEGER)")

    def insert_user(self, id, pwd):
        """
        插入一个用户
        """
        if self.select_user_by_id(id) is None:
            self.cur.execute("INSERT INTO user (id,pwd)VALUES ('{}', '{}')".format(id, pwd))
            self.conn.commit()
            return True
        else:
            return False

    def select_user_by_id(self, user_id):
        """
        根据id查找用户
        """
        row = self.cur.execute("SELECT id, pwd FROM user WHERE id='{}'".format(user_id)).fetchone()
        return row

    def select_player_status(self, key, id):
        """
        根据game key 和 id 查找玩家状态
        """
        row = self.cur.execute("SELECT * FROM playerstatus WHERE game_key='{}' and id='{}'".format(key, id)).fetchone()
        return row

    def insert_player_status(self, key, id, hp, bullet_amount, total_bullet):
        """
        插入玩家状态
        """
        if not self.select_player_status(key, id):
            self.cur.execute(
                "INSERT INTO playerstatus (game_key,id,hp,bullet_amount,total_bullet)VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                    key, id, hp, bullet_amount, total_bullet))
            self.conn.commit()
            return True
        else:
            # key 已经存在不能插入
            return False

    def update_player_status(self, key, id, hp, bullet_amount, total_bullet):
        """
        更新玩家状态
        """
        if self.select_player_status(key, id):
            self.cur.execute(
                "UPDATE playerstatus SET hp='{}',bullet_amount='{}',total_bullet='{}'WHERE game_key='{}' and id='{}'".format(
                    hp, bullet_amount, total_bullet, key, id))
            self.conn.commit()
            return True
        else:
            return False


dbManager = DBManager()

if __name__ == '__main__':
    db = DBManager()
    # db.insert_user("111", "pwd")
    print dbManager.select_user_by_id('111')[0]
