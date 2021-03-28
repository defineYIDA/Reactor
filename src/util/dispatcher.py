# encoding=utf8


class Dispatcher:
    """
    调度器，用来进行任务分发
    """

    def __init__(self):
        self._eventHandler_dict = {}

    def handler_event(self, command, conn, msg):
        """
        根据Command 进行事件分发
        """
        if command in self._eventHandler_dict:
            self._eventHandler_dict[command](conn, msg)

    def register_handler(self, command, handler):
        """
        注册处理函数
        """
        if command in self._eventHandler_dict:
            self._eventHandler_dict[command] = handler
        else:
            self._eventHandler_dict[command] = handler

    def remove_handler(self, command):
        """
        移除处理函数
        """
        if command in self._eventHandler_dict:
            self._eventHandler_dict.pop(command)


# 单例
Dispatcher = Dispatcher()
