# encoding=utf8

from msg import Msg


class LoginMsg(Msg):
    """
    data:
    {
      "id": "",
      "pwd": "",
    }
    """

    def __init__(self, data):
        self._data = data

    def get_command(self):
        return 1
