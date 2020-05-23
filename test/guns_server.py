# encoding=utf8

import tcp_server
from dispatcher import Dispatcher

class GunsServer(tcp_server.TcpServer):
    def __init__(self):
        # 调用父类构造进行Server的初始化
        super(GunsServer, self).__init__(('', 8080), time_out=10)

        # 初始化调度器
        self._init_Dispatcher()

    def on_message(self, tcp_connection, commend, msg):
        """
        message就绪进行分发
        """
        Dispatcher.HandlerEvent(commend, tcp_connection, msg)

    def write_complete(self):
        print 'server write done!'


    def _init_Dispatcher(self):
        """
        初始化
        """
        # 登陆消息
        Dispatcher.RegisterHandler(1,self._login_handler)

    def _login_handler(self, tcp_connection, msg):
        """
        login msg的处理函数
        """
        print msg.get_command()
        print str(msg.data)
        print msg.data['id']
        print msg.data['pwd']
        tcp_connection.send(msg)


if __name__ == '__main__':
    import waker, thread, time, timer
    server_ins = GunsServer()
    server_ins.run()
