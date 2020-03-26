# encoding=utf8

import tcp_server


class TestServer(tcp_server.TcpServer):
    def on_message(self, tcp_connection, buffer):
        print buffer.get_all()

    def write_complete(self):
        print 'server write done!'


def test(waker):
    import time
    time.sleep(2)
    waker.wake_up()
    # while True:
    #     time.sleep(2)
    #     waker.wake_up()


if __name__ == '__main__':
    import waker, thread, time, timer

    server_ins = TestServer(('', 8080), time_out=10)
    # waker = waker.SocketWaker(server_ins.loop)
    waker = waker.waker(server_ins.loop)
    # thread.start_new_thread(test, (waker,))
    server_ins.loop.add_timer(timer.Timer(0, waker.wake_up))
    server_ins.run()
