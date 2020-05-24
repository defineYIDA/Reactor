# encoding=utf8

import tcp_server
from dispatcher import Dispatcher
from command import Command


class GunsServer(tcp_server.TcpServer):
    def __init__(self):
        # 调用父类构造进行Server的初始化
        super(GunsServer, self).__init__(('', 8080), time_out=1)

        # 初始化调度器
        self._init_Dispatcher()

    def on_message(self, tcp_connection, commend, msg):
        """
        message就绪进行分发
        """
        Dispatcher.HandlerEvent(commend, tcp_connection, msg)

    def write_complete(self):
        print 'server write done!' + str(time.time())

    def _init_Dispatcher(self):
        """
        初始化
        """
        # 客户端心跳
        Dispatcher.RegisterHandler(Command.HEARTBEAT, self.client_heart_beat_handler)
        # 登陆消息
        Dispatcher.RegisterHandler(Command.LOGIN_REQUEST, self._login_handler)

    def _login_handler(self, tcp_connection, msg):
        """
        login msg的处理函数
        """
        print msg.get_command()
        print msg.data['id']
        print msg.data['pwd']

        # 构建响应报文
        from login_res_msg import LoginResMsg
        res_msg = LoginResMsg({
            "id": msg.data['id'],
            "status": "true",
            "msg": "login success"
        })
        tcp_connection.send(res_msg)


if __name__ == '__main__':
    import waker, thread, time, timer

    server_ins = GunsServer()
    server_ins.heart_beat()
    server_ins.run()
