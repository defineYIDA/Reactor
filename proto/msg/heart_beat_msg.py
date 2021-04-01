# encoding=utf8

from proto.msg.msg import Msg
from proto.msg.command import Command


class HeartBeatMsg(Msg):
    """心跳消息"""
    def __init__(self):
        super(HeartBeatMsg, self).__init__(Command.HEARTBEAT)
