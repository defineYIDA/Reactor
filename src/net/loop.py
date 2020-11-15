# encoding=utf8
import poller
import threading
import Queue
import timer
import waker


class EventLoop(object):
    """
    事件循环
    """

    def __init__(self, timeout):
        self._poller = poller.poller()  # 根据环境选择支持的poller
        self._timer_queue = timer.TimerQueue(self)  # 定时器
        self._waker = waker.waker(self)  # 对 wake up 的支持

        self.is_running = False
        self._timeout = timeout  # 轮询的阻塞时间
        self._thread_id = threading.currentThread()  # 当前线程id

        self.event_fun_queue = Queue.Queue()  # 事件队列需要在主线程中执行
        self.is_excuting_event = False

    def local_thread(self):
        # 当前线程是否是reactor的主线程
        return self._thread_id == threading.currentThread()

    def add_event_fun(self, fun_with_args):
        # 向事件队列中添加事件函数
        self.event_fun_queue.put(fun_with_args)

        if not self.local_thread() or self.is_excuting_event:
            # 当其他线程添加事件时唤醒poller
            self._waker.wake_up()  # 唤醒poller

    def excute_event_fun(self):
        self.is_excuting_event = True

        count = self.event_fun_queue.qsize()
        while count > 0:
            fun, calle_ins, args, kwargs = self.event_fun_queue.get()
            fun(calle_ins, *args, **kwargs)
            count -= 1

        self.is_excuting_event = False

    def loop(self):
        if not self.local_thread():
            # 创建线程才能执行
            return

        while self.is_running:
            active_list = self._poller.poll(self._timeout)

            for channel in active_list:
                # 执行就绪回调
                channel.handle_event()

            # 处理计时任务
            self._timer_queue.schedule()

            # 执行队列中的事件
            self.excute_event_fun()

    def update_channel(self, channel):
        self._poller.update_channel(channel)

    def remove_channel(self, channel):
        self._poller.remove_channel(channel)

    def add_timer(self, timer):
        self._timer_queue.add_timer(timer)

    def remove_timer(self, timer_id):
        self._timer_queue.remove_timer(timer_id)
