# encoding=utf8
class ConnectorState(object):
    """
    执行非阻塞connect 过程中 的状态
    """
    CONNECTED = 0
    CONNECTING = 1
    ERROR = 2
