# encoding=utf8

from msg import Msg
from command import Command


class RegisterResMsg(Msg):
    """
    登陆响应报文
    data:
    {
      "id": "",
      "status": "",
      "msg": "",
    }
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.REGISTER_RESPONSE
