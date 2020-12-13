# encoding=utf8

from packet import Packet


class MessagePacket(Packet):

    def __init__(self, msg):
        self.msg = msg

    def get_command(self):
        return 1

    def get_message(self):
        return self.msg
