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
