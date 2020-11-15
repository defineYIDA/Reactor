# encoding=utf8
from conf import Conf


class RoomQueue(object):
    """
    房间队列，采用生产消费模式创建房间
    """

    def __init__(self):
        import Queue
        from room_manager import room_manager
        self._queue = Queue.Queue()  # 加入房间的队列，接收到用户的加房指令就会将用户放到这个队列

        self._user_wait_time = 0  # 队列中第一个玩家的进入时间

        self._room_manager = room_manager  # 房间管理

    def add_wait(self, user_id):
        """
        添加到等待队列
        :param user_id:
        :return:
        """
        import time
        if self._queue.empty():
            self._user_wait_time = time.time()
        self._queue.put(user_id)

    def work(self):
        import time
        while True:
            now = time.time()
            # print self._queue.qsize()
            # print self._user_wait_time
            if self._queue.empty() or self._user_wait_time == 0:
                # 没有玩家在匹配
                continue
            elif (now - Conf.CREAT_ROOM_WAIT_TIME >= self._user_wait_time) or (self._queue.qsize() >= Conf.ROOM_LIMIT):
                # 超过创建房间的等待时间 or 到达房间人数
                # 清空队列，创建房间 添加到房间管理，发送房间创建好的指令
                user_list = []
                while not self._queue.empty():
                    user_list.append(self._queue.get())
                room_id = "r:" + str(now)  # 房间id
                self._room_manager.create_room(room_id, user_list)  # 创建房间
                self._user_wait_time = 0


import threading

# 单例对象
room_queue = RoomQueue()
room_queue_thread = threading.Thread(target=room_queue.work)
room_queue_thread.start()