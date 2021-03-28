# encoding=utf8


class RoomManager(object):

    def __init__(self):
        self.room_map = {}  # 房间<room_id,list<game_status>>

    def create_room(self, room_id, user_list):
        """
        创建房间
        :param room_id:
        :param user_list:
        :return:
        """
        if room_id not in self.room_map and user_list:
            import json
            from join_room_res_msg import JoinRoomResMsg
            from game_status import GameStatus
            from conf import Conf

            info_list = []
            for user_id in user_list:
                info_list.append(GameStatus(user_id, Conf.WARRIOR, Conf.WAIT_JOIN))
            self.room_map[room_id] = info_list
            print str(self.room_map)

            # 构建创建房间成功消息
            res_msg = JoinRoomResMsg({
                'room_id': room_id,
                'status': 'true',
                'data': json.dumps(user_list)
            })
            self.send_room_msg(room_id, res_msg)
            return True
        else:
            return False

    def change_player_status(self, user_id, room_id, status):
        """
        更改玩家状态
        :param user_id:
        :param room_id:
        :param status:
        :return:
        """
        user_list = self.room_map[room_id]

        for user in user_list:
            if user.user_id == user_id:
                user.status = status

    def check_scenes_status(self, room_id):
        """
        检查玩家场景加载状态
        :param room_id:
        :return:
        """
        from conf import Conf

        user_list = self.room_map[room_id]
        for user in user_list:
            if user.status != Conf.SCENE_LOAD:
                return False
        return True

    def check_game_status(self, room_id):
        """
        检查游戏状态，只有一个存活玩家时游戏结束
        :param room_id:
        :return:
        """
        from conf import Conf

        user_list = self.room_map[room_id]
        count = 0
        for user in user_list:
            if user.status == Conf.ALIVE:
                count += 1
        return count == 0 or count == 1

    def del_room(self, room_id):
        """
        删除房间
        :param room_id:
        :return:
        """
        if self.room_map.has_key(room_id):
            del self.room_map[room_id]

    def send_room_msg(self, room_id, msg):
        """
        发送消息到房间内所有玩家
        :return:
        """
        from online_manager import online_manager

        if room_id not in self.room_map:
            return False

        user_list = self.room_map[room_id]

        # 构建对象的初始化信息（位置，旋转）
        for user in user_list:
            online_manager.send_msg_to_user(user.user_id, msg)
        return True

    def send_msg_to_room_other_player(self, curr_id, room_id, msg):
        """
        发送消息到房间内其他玩家
        :param user_id:
        :param room_id:
        :param msg:
        :return:
        """
        from online_manager import online_manager

        if room_id not in self.room_map:
            return False

        user_list = self.room_map[room_id]

        # 构建对象的初始化信息（位置，旋转）
        for user in user_list:
            # 判断当前用户
            if user.user_id == curr_id:
                continue
            online_manager.send_msg_to_user(user.user_id, msg)
        return True

    def count_rank(self, user_id, room_id):
        """
        计算死亡的玩家的排名
        :param user_id:
        :param room_id:
        :return:
        """
        from conf import Conf

        if room_id not in self.room_map:
            return -1
        user_list = self.room_map[room_id]

        curr_user = None
        count = len(user_list)
        for user in user_list:
            if user.user_id != user_id and user.status == Conf.DIE:
                count -= 1
            elif user.user_id == user_id:
                curr_user = user

        curr_user.status = Conf.DIE
        return count





# 单例对象
room_manager = RoomManager()
