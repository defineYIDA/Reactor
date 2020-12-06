# encoding=utf8


class RunInLoop(object):
    """
    loop 包装器
    作用：1）func所属类中是否有loop
        2）是否在主线程中调用
    """

    def __init__(self, func):
        self._func = func
        self._loop = None
        self._call_ins = None

    def __get__(self, ins, owner):
        if ins and '_loop' in ins.__dict__:
            self._call_ins = ins
            self._loop = ins.__dict__['_loop']
        else:
            # func的类中没有loop，报错
            LOG.error("call class:{} error ! not exist 'loop".format(type(ins)))
        return self

    def __call__(self, *args, **kwargs):
        if self._loop.local_thread():
            # 在主线程中
            self._func(self._call_ins, *args, **kwargs)
        else:
            # 不在主线程中，添加到事件队列，例如业务线程执行一个send
            self._loop.add_event_fun((self._func, self._call_ins, args, kwargs))
