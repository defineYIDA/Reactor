# encoding=utf8

from msg import Msg
from command import Command


class GetSettingResMsg(Msg):
    """
    登陆响应报文
    data:
    {
      "status": "",
      "data": "",
      "type": "",
    }
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.GET_SETTING_RESPONSE
