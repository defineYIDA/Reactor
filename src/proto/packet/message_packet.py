# encoding=utf8

from packet import Packet


class MessagePacket(Packet):

    def __init__(self, msg):
        self.msg = msg

    def get_command(self):
        return 1

    def get_message(self):
        return self.msg


if __name__ == '__main__':
    m = MessagePacket("hello!!!")
    print m.get_command()
    import cPickle
    d = cPickle.dumps(m, -1)
    #print d
    print cPickle.loads(d).get_command()