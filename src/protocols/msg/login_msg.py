# encoding=utf8

from msg_base import MsgBase


class LoginMsg(MsgBase):
    """
    data:
    {
      "id": "",
      "pwd": "",
    }
    """

    def get_command(self):
        return self.command
