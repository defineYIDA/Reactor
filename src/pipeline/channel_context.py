# encoding=utf8


class ChannelContext(object):

    def __init__(self, conn, pipeline):
        """conn处理的上下文"""
        import weakref
        self.conn = weakref.ref(conn)
        self.pipe = pipeline

    def write_and_flush(self, msg):
        """直接出站
        """
        if self.pipe:
            self.pipe.outbound_process(self, msg)
    
    def direct_send(self, msg):
        """直接发送
        """
        if not msg:
            return
        codec = self.get_codec()
        if not codec:
            self.conn().send(msg)
        else:
            self.conn().send(codec.encode(msg))

    def get_splitter(self):
        """获得拆包器"""
        return self.pipe.splitter if self.pipe else None

    def get_codec(self):
        """获得编解码器"""
        return self.pipe.codec if self.pipe else None
