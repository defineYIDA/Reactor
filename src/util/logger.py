# encoding=utf8


class LoggerQueue(object):
    """
    日志队列，负责异步的生成日志文件
    """

    def __init__(self, log_internal=3600 * 24, log_dir='log', log_basename='log'):
        import Queue, time, os
        self.queue = Queue.Queue()  # 需要写到文件的日志
        self._log_dir = log_dir
        self._log_basename = log_basename

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        self._log_start_time = time.time()
        self._log_internal = log_internal

        self._filename = self._get_filename()

    def _get_filename(self):
        import datetime, os
        return '{}_{}'.format(os.path.join(self._log_dir, self._log_basename),
                              datetime.datetime.fromtimestamp(self._log_start_time).strftime("%Y-%m-%d"))

    def work(self):
        import time
        while True:
            log = self.queue.get()  # 阻塞
            now = time.time()

            if now - self._log_internal > self._log_start_time:
                # 超过间隔新开一个日志（默认间隔为一天）
                self._log_start_time = now
                self._filename = self._get_filename()

            # 写日志到文件
            wfp = open(self._filename, 'a')
            wfp.write(log)
            wfp.close()
            self.queue.task_done()


import threading

# 日志的队列是一个单例对象，独占一个工作线程，负责写日志到文件
logger_queue = LoggerQueue()
logger_queue_thread = threading.Thread(target=logger_queue.work)
logger_queue_thread.setDaemon(True)
logger_queue_thread.start()


class Logger(object):
    """
    异步日志
    """

    def __init__(self, flush_internal=0, buffer_len_bound=1024):
        """
        flush_internal:默认为0，代表每一个log都会立即放到log 队列中，写入文件
        如果大于0会出现第一个日志写入不到文件的问题
        """
        import cStringIO, time

        self._logger = None
        self._thread = None

        self._logger_queue = logger_queue.queue

        self._last_flush_time = time.time()
        self._flush_internal = flush_internal  # 缓冲区刷新间隔

        self._buffer = cStringIO.StringIO()  # 缓冲区
        self._buffer_len_bound = buffer_len_bound  # 缓冲区上限，到达上限需写日志文件
        self._buffer_len = 0

        self._fmt = "%(asctime)s	%(thread)d	%(levelname)s	%(pathname)s:%(lineno)d	%(message)s"
        self._create_logger()

    def _create_logger(self):
        import logging

        if self._logger:
            return

        # 创建logger
        logger_name = 'logger'
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(logging.DEBUG)

        # 异步写日志到文件
        log_file_handler = logging.StreamHandler(self._buffer)
        log_file_handler.setFormatter(logging.Formatter(self._fmt))

        # console 打印log
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(self._fmt))

        # 设置handler
        self._logger.addHandler(log_file_handler)
        self._logger.addHandler(console_handler)

    def write_log(self, log_message, level, sync=False):
        """
        写入日志文件，会执行在主线程，通过队列异步处理防止对主线程的阻塞
        sync: 是否阻塞至缓冲区全部写入文件
        """
        import logging, time, sys

        call_frame = sys._getframe().f_back  # 获取调用write_log 的pyFrameObject

        # 获取事发地点的文件名,行号和函数名
        fn, lno, func = call_frame.f_code.co_filename, call_frame.f_lineno, call_frame.f_code.co_name

        log_record = self._logger.makeRecord(self._logger.name, logging._levelNames[level.upper()],
                                             fn=fn, lno=lno, msg=log_message,
                                             args=None, exc_info=None, func=func, extra=None)

        # 处理日志记录
        self._logger.handle(log_record)  # log记录写入buffer

        self._buffer_len = self._buffer.tell()

        now = time.time()
        if sync:
            self._flush()
            self._last_flush_time = now
            self._logger_queue.join()  # 阻塞直到日志队列为空

        elif self._buffer_len >= self._buffer_len_bound or now - self._last_flush_time > self._flush_internal:
            # 缓冲区满 or 刷新间隔
            self._flush()
            self._last_flush_time = now

    def _flush(self):
        self._logger_queue.put(self._buffer.getvalue())
        self._buffer.seek(0)
        self._buffer.truncate()  # 裁剪清除所有数据
        self._buffer_len = 0


if __name__ == '__main__':
    import time, logging

    start = time.time()
    logger = Logger(flush_internal=3, buffer_len_bound=20480)
    i = 0
    while i < 100000:
        logger.write_log("hello world {}".format(i), 'error')
        i += 1
    delta = time.time() - start
    print delta

    # 对比,效率主要区别在文件打开次数上
    start = time.time()
    logger_name = 'simple_logger'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('test.log')
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s	%(thread)d	%(levelname)s	%(pathname)s:%(lineno)d	%(message)s"))
    logger.addHandler(file_handler)
    i = 0
    while i < 100000:
        logger.error("hello world {}".format(i))
        i += 1

    delta = time.time() - start
    print delta