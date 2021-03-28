# encoding=utf8
import sys,os
sys.path.append(os.path.realpath('.'))

if __name__ == '__main__':
    import time
    from src.net.loop import EventLoop
    from src.util.timer import Timer, TimerQueue
    from src.util.logger import Logger

    Logger.start_logger_service()
    timer_queue = TimerQueue(EventLoop(0.01))


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