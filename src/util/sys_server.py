# encoding=utf8


class SystemServer(object):
    """
    系统服务类，用于处理服务端和客户端的心跳和空闲检测
    """

    def __init__(self, logger, loop):
        self._logger = logger
        self._loop = loop

        self._handler_map = {}  # {系统消息类型，处理函数}

    # def register_sys_msg_handler(self, sys_msg_type, handler_func):
    #     """
    #     注册系统消息和对应的处理函数
    #     """
    #     if sys_msg_type in self._handler_map:
    #         self._logger.write_log('sys_msg %d has been registered' % sys_msg_type,'error')
    #     else:
    #         pass

    def register_timer_handler(self, internal, func):
        """
        注册一个timer
        """
        import timer, time
        tme = timer.Timer(internal, func)
        self._loop.add_timer(tme)
        return tme.timer_id

    def remove_timer(self, timer_id):
        """
        移除timer
        """
        self._loop.remove_timer(timer_id)


class ServerHeartBeatServer(object):
    """
    服务端心跳服务
    """

    def __init__(self, system_service_center, conn_map, internal=1):
        self._system_service_center = system_service_center
        self.heartbeat_internal = internal
        self._conn_map = conn_map

    def register(self):
        """
        将发送心跳包的定时任务注册
        """
        self._system_service_center.register_timer_handler(self.heartbeat_internal, self.send_heartbeat)

    def send_heartbeat(self):
        """
        向所有客户端连接发送心跳
        """
        import time
        from heart_beat_msg import HeartBeatMsg

        # 失活客户端连接
        del_list = []
        for item in self._conn_map.iteritems():
            conn_key = item[0]
            tcp_connection = item[1]
            # 空闲检测
            if time.time() - tcp_connection.last_recv_heart_time > self.heartbeat_internal * 3:
                del_list.append(conn_key)
            else:
                tcp_connection.send(HeartBeatMsg())

        # 关闭失活连接
        for conn_key in del_list:
            tcp_connection = self._conn_map[conn_key]
            tcp_connection.handle_close()
