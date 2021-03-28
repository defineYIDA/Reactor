# encoding=utf8
import time
import json
from room_manager import room_manager
from conf import Conf


class PlayerInfoHandler(object):
    """"
    玩家消息处理
    """

    def __init__(self):
        pass

    def join_room_handler(self, tcp_connection, msg):
        from room_queue import room_queue
        print "join room"
        # 加入房间的等待
        # room_manager.add_player_character(msg.data['id'], msg.data['character'])
        room_queue.add_wait(msg.data['id'])
        print "recv player join room info" + str(time.time()) + "[" + msg.data['id'] + "]"

    def player_status_info_handler(self, tcp_connection, msg):
        """
        游戏内状态消息
        :param tcp_connection:
        :param msg:
        :return:
        """
        from player_info_res_msg import PlayerInfoResMsg

        res_msg = PlayerInfoResMsg({
            'status': 'true',
            'type': Conf.STATUS_REQ,
            'data': msg.data['data']
        })
        room_manager.send_msg_to_room_other_player(msg.data['id'], msg.data['room_id'], res_msg)

    def player_create_info_handler(self, tcp_connection, msg):
        """
        创建玩家消息
        :param tcp_connection:
        :param msg:
        :return:
        """
        from player_info import PlayerInfo
        from player_info_res_msg import PlayerInfoResMsg

        # 构建玩家初始化信息
        character = msg.data['data']  # 角色
        info = PlayerInfo(msg.data['id'], character)
        info.set_random_pos()  # 设置一个随机位置
        res_msg = PlayerInfoResMsg({
            'status': 'true',
            'type': Conf.CREATE_REQ,
            'data': json.dumps(info.dict)
        })
        print "recv create player" + str(time.time()) + "[" + msg.data['id'] + "]"
        room_manager.send_room_msg(msg.data['room_id'], res_msg)
        print "send create player" + str(time.time()) + "[" + msg.data['id'] + "]"


    def player_scenes_load_handler(self, tcp_connection, msg):
        """
        游戏场景加载成功消息，当房间内最后一个玩家加载好场景
        通知房间内玩家创建发送创建角色消息
        :param tcp_connection:
        :param msg:
        :return:
        """
        room_manager.change_player_status(msg.data['id'], msg.data['room_id'], Conf.SCENE_LOAD)
        # 判断房间内所有玩家的场景是否加载完成
        if room_manager.check_scenes_status(msg.data['room_id']):
            from player_info_res_msg import PlayerInfoResMsg
            # 发送可以创建玩家的消息
            res_msg = PlayerInfoResMsg({
                'status': 'true',
                'type': Conf.SCENES_REQ,
                'data': "{}"
            })
            room_manager.send_room_msg(msg.data['room_id'], res_msg)
            print "Scenes Load create player" + str(time.time())
