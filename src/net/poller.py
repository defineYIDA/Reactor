# encoding=utf8
import select
import platform
from src.util import error


class PollerBase(object):
    """
    不同的操作系统对多路复用的支持不同
    win不支持epoll，而select具有良好的平台兼容性
    """

    def __init__(self):
        self.channel_map = {}  # 需要监测的channel

    def poll(self, timeout):
        raise NotImplementedError

    def update_channel(self, channel):
        self.channel_map[channel.fd] = channel

    def remove_channel(self, channel):
        if self.channel_map.has_key(channel.fd):
            del self.channel_map[channel.fd]


class SelectPollerBase(PollerBase):
    """
    对select支持
    """

    def poll(self, timeout):
        active_list = []  # 轮询到就绪的channel

        if not self.channel_map or len(self.channel_map) == 0:
            return active_list

        r_list = []
        w_list = []
        x_list = []

        for fd in self.channel_map:
            channel = self.channel_map[fd]
            if channel.need_read:
                r_list.append(fd)

            if channel.need_write:
                w_list.append(fd)

            if channel.need_read or channel.need_write:
                # 异常监测
                x_list.append(fd)

        if not r_list and not w_list and not x_list:
            return active_list

        try:
            import time
            # s = time.time()
            r_list, w_list, x_list = select.select(r_list, w_list, x_list, timeout)

        except select.error, e:
            if e.args[0] == error.EINTR:
                # 阻塞中断，因为会出现对wakeup的支持
                return active_list
            else:
                print e.message
                raise
        # print 'time:' + str(time.time() - s)
        for rfd in r_list:
            channel_ins = self.channel_map[rfd]
            channel_ins.readable = True
            active_list.append(channel_ins)

        for wfd in w_list:
            channel_ins = self.channel_map[wfd]
            channel_ins.writable = True
            active_list.append(channel_ins)

        for efd in x_list:
            channel_ins = self.channel_map[efd]
            channel_ins.error = True
            active_list.append(channel_ins)

        return active_list


if platform.system() == 'Windows':
    Poller = SelectPollerBase
else:
    # TODO 不同环境下对其他复用函数的支持
    Poller = SelectPollerBase
