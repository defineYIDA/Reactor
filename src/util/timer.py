# encoding=utf8
import loop_decorator


class Timer(object):
    """
    定时器
    """
    timer_seq = 0

    def __init__(self, internal, method, *args, **kwargs):
        import time
        self.internal = internal  # 执行间隔
        self.excute_time = time.time() + internal  # 当前事件+间隔后执行第一次

        self._method = method
        self._args = args
        self._kwargs = kwargs

        self.timer_id = Timer.timer_seq
        Timer.timer_seq += 1

        self.cancel = False

    @property
    def repeatable(self):
        """
        （由于当前计时器不是独立线程，受select的阻塞时间影响）
        internal > 0 间隔internal执行一次
        internal == 0 每一次阻塞结束后执行
        internal < 0 执行一次
        """
        return self.internal >= 0

    def excute_event(self):
        self._method(*self._args, **self._kwargs)

    def __le__(self, other):
        return self.excute_time <= other.excute_time


class TimerQueue(object):
    """
    存放定时事件的优先队列
    """

    def __init__(self, loop):
        import Queue
        self._loop = loop
        self._heap = Queue.PriorityQueue()
        self._cancel_count = 0

    def schedule(self):
        import time
        now = time.time()
        while not self._heap.empty():
            if now < self._heap.queue[0].excute_time:
                break

            timer = self._heap.get()
            assert isinstance(timer, Timer)

            if timer.cancel:
                # 当前timer已被取消，那么现在已经弹出删除
                self._cancel_count -= 1
                continue
            else:
                timer.excute_event()  # 执行计时事件
                if timer.repeatable:
                    # 需要重复执行
                    timer.excute_time = time.time() + timer.internal
                    self._heap.put(timer)

    @loop_decorator.RunInLoop
    def add_timer(self, timer):
        self._heap.put(timer)

    @loop_decorator.RunInLoop
    def remove_timer(self, timer_id):
        for timer in self._heap.queue:
            if timer.timer_id == timer_id:
                timer.cancel = True
                self._cancel_count += 1

        # 当标识取消的timer超过1/4 重建堆
        if self._cancel_count * 1.0 / self._heap.qsize() > 1 / 4:
            self.rebuild_heap()

    def rebuild_heap(self):
        """
        删除取消事件，重新建堆
        """
        import heapq
        tmp_list = []
        for timer in self._heap.queue:
            if not timer.cancel:
                tmp_list.append(timer)

        self._heap.queue = tmp_list
        heapq.heapify(self._heap.queue)
        self._cancel_count = 0


if __name__ == '__main__':
    import time, loop, logger

    timer_queue = TimerQueue(loop.EventLoop(0.01, logger.Logger()))


    def test_func():
        print 'hello'


    def test_func1():
        print 'hello repeat'


    timer_ins = Timer(0, test_func)
    print timer_ins.timer_id
    timer_ins1 = Timer(1, test_func1)
    print timer_ins1.timer_id
    timer_queue.add_timer(timer_ins)
    timer_queue.add_timer(timer_ins1)
    while 1:
        timer_queue.schedule()
        time.sleep(1)
    pass
