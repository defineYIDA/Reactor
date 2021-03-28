# encoding=utf8
from online_status import OnlineStatus


class OnlineManager(object):
    """
    在线用户的管理（为user_id和conn_key的映射）
    1)负责用户登录状态的判断

    """

    def __init__(self):
        self.online_status_map = {}  # 用户的登录状态
        self.online_map = {}  # 在线用户，Map<user_id, conn_key>

    def login(self, user_id, conn_key):
        """
        用户登录
        :param user_id:
        :param conn_key:
        :return: bool
        """
        # if self.online_status_map.has_key(user_id):
        #     if self.online_status_map[user_id] != OnlineStatus.NOT_ONLINE:
        #         return False

        self.online_status_map[user_id] = OnlineStatus.ONLINE
        self.online_map[user_id] = conn_key
        return True

    def login_out(self, user_id):
        """
        用户登出
        :param user_id:
        :return:
        """
        if self.online_status_map.has_key(user_id):
            del self.online_status_map[user_id]

        if self.online_map.has_key(user_id):
            del self.online_map[user_id]

    def _change_online_status(self, user_id, status):
        if self.online_status_map.has_key(user_id):
            self.online_status_map[user_id] = status

    def enter_room(self, user_id):
        """
        进入房间
        :param user_id:
        :return:
        """
        self._change_online_status(user_id, OnlineStatus.IN_ROOM)

    def exit_room(self, user_id):
        """
        退出房间
        :param user_id:
        :return:
        """
        self._change_online_status(user_id, OnlineStatus.ONLINE)

    def exit_game(self, user_id):
        self._change_online_status(user_id, OnlineStatus.NOT_ONLINE)
        if user_id in self.online_map:
            del self.online_map[user_id]

    def send_msg_to_user(self, user_id, msg):
        """
        发送消息到玩家
        :param user_id:
        :param msg:
        :return:
        """
        from wild_server import server_ins

        status = self.online_status_map[user_id]
        conn_key = self.online_map[user_id]
        if status != OnlineStatus.ONLINE:
            return False
        if conn_key not in server_ins.conn_map:
            return False
        conn = server_ins.conn_map[conn_key]  # 获得玩家对应的socket
        conn.send(msg)
        return True

    def check_login(self, user_id):
        from wild_server import server_ins
        conn_key = self.online_map[user_id]
        if conn_key is None:
            return True
        else:
            if conn_key not in server_ins.conn_map:
                return True
            else:
                return False



# 单例对象
online_manager = OnlineManager()
