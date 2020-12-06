# encoding=utf8


class ChannelContext(object):

    def __init__(self, conn, pipeline):
        """conn处理的上下文"""
        self.conn = conn
        self.pipe = pipeline
