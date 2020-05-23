# encoding=utf8


class MsgBase(object):
    """
    消息包协议
    """
    data = {}

    def __init__(self, command, data):
        if not data:
            self.data = {
                "id": "",
            }
        else:
            self.data = data
        self.command = command

    def get_command(self):
        return self.command
