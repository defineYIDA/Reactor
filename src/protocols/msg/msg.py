# encoding=utf8


class Msg(object):
    """
    msg协议
    """

    def get_command(self):
        raise NotImplementedError
