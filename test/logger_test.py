# encoding=utf8
def run_test():
    import time
    import logging
    from src.util.logger import Logger
    start = time.time()
    logger = Logger(flush_internal=3, buffer_len_bound=20480)
    i = 0
    while i < 100000:
        logger.error("hello world {}".format(i))
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

    # TEST version 2.0
    Logger.start_logger_service()
    LOG.error("TEST")