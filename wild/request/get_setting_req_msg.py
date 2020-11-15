# encoding=utf8

from msg import Msg
from command import Command


class GetSettingReqMsg(Msg):
    """
    获得设置参数请求报文
    data:
    {
      "id": "",
      "type": "",
    }
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.GET_SETTING_REQUEST
