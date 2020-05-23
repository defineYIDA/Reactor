# encoding=utf8


class Dispatcher:
    """
    调度器，用来进行任务分发
    """

    def __init__(self):
        self._eventHandlerDict = {}

    def HandlerEvent(self, command, conn, msg):
        """
        根据Command 进行事件分发
        """
        if self._eventHandlerDict.has_key(command):
            self._eventHandlerDict[command](conn, msg)

    def RegisterHandler(self, command, handler):
        """
        注册处理函数
        """
        if self._eventHandlerDict.has_key(command):
            self._eventHandlerDict[command] = handler
        else:
            self._eventHandlerDict[command] = handler

    def RemoveHandler(self, command):
        """
        移除处理函数
        """
        if self._eventHandlerDict.has_key(command):
            self._eventHandlerDict.pop(command)


# 单例
Dispatcher = Dispatcher()