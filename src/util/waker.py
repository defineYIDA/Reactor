# encoding=utf8


class waker(object):
    def __init__(self):
        pass

    def wake_up(self):
        raise NotImplementedError


class PipeWaker(waker):
    def wake_up(self):
        print ""
        pass


waker = PipeWaker
