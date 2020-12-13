# encoding=utf8


class ChannelContext(object):

    def __init__(self, conn, pipeline):
        """conn处理的上下文"""
        self.conn = conn
        self.pipe = pipeline
        self.packet_ready = False  # 表示完整协议包可能就绪

    def flush(self):
        pass
