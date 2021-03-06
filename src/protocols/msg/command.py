# encoding=utf8


class Command(object):
    """
    协议所有包对应的Command常量
    """
    # 心跳
    HEARTBEAT = 0
    # 登陆请求
    LOGIN_REQUEST = 1
    # 登陆响应
    LOGIN_RESPONSE = 2
    # 注册请求
    REGISTER_REQUEST = 3
    # 注册响应
    REGISTER_RESPONSE = 4
    # 获取设置参数请求
    GET_SETTING_REQUEST = 5
    # 获取设置参数响应
    GET_SETTING_RESPONSE = 6
    # 获取玩家状态请求
    GET_PLAYER_STATUS_REQUEST = 7
    # 获取玩家状态响应
    GET_PLAYER_STATUS_RESPONSE = 8
    # 玩家事件请求
    EVENT_REQUEST = 9
    # 玩家事件请求响应
    EVENT_RESPONSE = 10
