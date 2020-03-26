# encoding=utf8


class RunInLoop(object):
    """
    loop 包装器
    作用：1）func所属类中是否有loop
        2）是否在主线程中调用
    """

    def __init__(self, func):
        self.func = func
        self._loop = None
        self.calle_ins = None

    def __get__(self, instance, owner):
        if instance and '_loop' in instance.__dict__:
            self.calle_ins = instance
            self._loop = instance._loop

        else:
            # func的类中没有loop，报错
            pass
        return self

    def __call__(self, *args, **kwargs):
        if self._loop.local_thread():
            # 在主线程中
            self.func(self.calle_ins, *args, **kwargs)
        else:
            # 不在主线程中，添加到事件队列，例如业务线程执行一个send
            self._loop.add_event_fun((self.func, self.calle_ins, args, kwargs))
