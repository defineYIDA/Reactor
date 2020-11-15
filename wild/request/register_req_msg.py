# encoding=utf8

from msg import Msg
from command import Command


class RegisterReqMsg(Msg):
    """
    登陆请求报文
    data:
    {
      "id": "",
      "pwd": "",
    }
    """

    def __init__(self, data):
        self.data = data

    def get_command(self):
        return Command.REGISTER_REQUEST
