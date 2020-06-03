# encoding=utf8
import os
import sys

sys.path.append(sys.path[0] + '/guns')
sys.path.append(os.path.dirname(sys.path[0]) + '/src/net')
sys.path.append(os.path.dirname(sys.path[0]) + '/src/protocols')
sys.path.append(os.path.dirname(sys.path[0]) + '/src/protocols/msg')
sys.path.append(os.path.dirname(sys.path[0]) + '/src/protocols/packet')
sys.path.append(os.path.dirname(sys.path[0]) + '/src/protocols/msg/request')
sys.path.append(os.path.dirname(sys.path[0]) + '/src/protocols/msg/response')
sys.path.append(os.path.dirname(sys.path[0]) + '/src/tcp')
sys.path.append(os.path.dirname(sys.path[0]) + '/src/util')

import tcp_server
from dispatcher import Dispatcher
from command import Command
from db_manager import dbManager
from player_status import PlayerStatus


class GunsServer(tcp_server.TcpServer):
    def __init__(self):
        # 调用父类构造进行Server的初始化
        super(GunsServer, self).__init__(('', 8080), time_out=1)

        # 初始化调度器
        self._init_Dispatcher()

    def on_message(self, tcp_connection, commend, msg):
        """
        message就绪进行分发
        """
        Dispatcher.HandlerEvent(commend, tcp_connection, msg)

    def write_complete(self):
        pass
        # print 'server write done!' + str(time.time())

    def _init_Dispatcher(self):
        """
        初始化
        """
        # 客户端心跳
        Dispatcher.RegisterHandler(Command.HEARTBEAT, self.client_heart_beat_handler)
        # 登陆消息
        Dispatcher.RegisterHandler(Command.LOGIN_REQUEST, self._login_handler)
        # 注册消息
        Dispatcher.RegisterHandler(Command.REGISTER_REQUEST, self._register_handler)
        # 获得设置参数消息
        Dispatcher.RegisterHandler(Command.GET_SETTING_REQUEST, self._get_setting_handler)
        # 获得玩家状态消息
        Dispatcher.RegisterHandler(Command.GET_PLAYER_STATUS_REQUEST, self._get_player_status_handler)
        # 玩家事件处理
        Dispatcher.RegisterHandler(Command.EVENT_REQUEST, self._event_handler)

    def _login_handler(self, tcp_connection, msg):
        """
        login msg的处理函数
        """
        from login_res_msg import LoginResMsg

        user = dbManager.select_user_by_id(msg.data['id'])
        if user:
            if msg.data['pwd'] == user[1]:
                # 生成对局key
                game_key = msg.data['id'] + str(time.time())
                # 数据库保存该对局的信息
                PlayerStatus.insert_player_status(game_key, msg.data['id'])
                # 构建响应报文
                res_msg = self._make_res_msg(LoginResMsg, msg.data['id'], "true", game_key)
            else:
                res_msg = self._make_res_msg(LoginResMsg, msg.data['id'], "false", "密码错误")
        else:
            res_msg = self._make_res_msg(LoginResMsg, msg.data['id'], "false", "登陆失败，用户id不存在")

        tcp_connection.send(res_msg)

    def _register_handler(self, tcp_connection, msg):
        """
        注册消息的处理函数
        """
        from register_res_msg import RegisterResMsg

        if dbManager.insert_user(msg.data['id'], msg.data['pwd']):
            # 构建响应报文
            res_msg = self._make_res_msg(RegisterResMsg, msg.data['id'], "true", "注册成功")
        else:
            res_msg = self._make_res_msg(RegisterResMsg, msg.data['id'], "false", "ID 存在")

        tcp_connection.send(res_msg)

    def _make_res_msg(self, msg_type, id, status, msg):
        """
        构建通用的响应消息
        """
        return msg_type({
            "id": id,
            "status": status,
            "msg": msg})

    def _get_setting_handler(self, tcp_connection, msg):
        """
        获得设置参数
        """
        import setting, json
        from get_setting_res_msg import GetSettingResMsg
        # TODO 判断id的登陆状态
        if msg.data['type'] == 'player':
            # 获得玩家的参数
            res_msg = GetSettingResMsg({
                'status': 'true',
                'type': 'player',
                'data': json.dumps(setting.PlayerSetting().dict)
            })
        elif msg.data['type'] == 'enemy':
            # 获得敌人的参数
            res_msg = GetSettingResMsg({
                'status': 'true',
                'type': 'enemy',
                'data': json.dumps(setting.EnemySetting().dict)
            })
        else:
            # 获取的参数不存在
            res_msg = GetSettingResMsg({
                'status': 'false',
                'type': msg.data['type'],
                'data': {}
            })

        if res_msg:
            tcp_connection.send(res_msg)

    def _get_player_status_handler(self, tcp_connection, msg):
        """
        获取玩家状态
        """
        from get_player_status_res_msg import GetPlayerStatusResMsg
        row = PlayerStatus.get_player_status(msg.data['key'], msg.data['id'])
        if row:
            res_msg = GetPlayerStatusResMsg(row)
        else:
            res_msg = GetPlayerStatusResMsg(None)
        tcp_connection.send(res_msg)

    def _event_handler(self, tcp_connection, msg):
        """
        玩家事件处理
        """
        key = msg.data['key']
        id = msg.data['id']
        type = msg.data['type']
        print 'event type' + str(type) + 'key: ' + key
        if type == 0:
            PlayerStatus.damage(key, id)
        elif type == 1:
            PlayerStatus.shoot(key, id)
        elif type == 2:
            PlayerStatus.reload(key, id)
        else:
            pass


if __name__ == '__main__':
    import time

    server_ins = GunsServer()
    server_ins.heart_beat()
    server_ins.run()
