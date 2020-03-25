# encoding=utf8


class TcpClient(object):
    """
    tcp client
    """

    def __init__(self, timeout):
        import connector, loop
        self.loop = loop.EventLoop(timeout)
        self.tcp_conn = None
        self.connector = connector.Connector(self.loop)
        self.connector.set_new_conn_callback(self.new_connection)

    def run(self):
        self.loop.is_running = True
        self.loop.loop()

    def connect(self, dst_addr):
        self.connector.connect(dst_addr)

    def disconnect(self):
        if self.tcp_conn:
            self.tcp_conn.shutdown()

    def new_connection(self, conn_socket, peer_addr):
        import tcp_connection, time
        # client连接成功时调用
        conn_key = '{}#{}#{}'.format(str(conn_socket.getsockname()), str(peer_addr), str(time.time()))
        self.tcp_conn = tcp_connection.TcpConnection(self.loop, conn_socket, conn_key)

        self.tcp_conn.set_message_callback(self.on_message)
        self.tcp_conn.set_write_complete_callback(self.write_complete)

    def send(self, data):
        if self.tcp_conn:
            self.tcp_conn.send(data)
        else:
            print '连接建立失败不能发送消息'

    def on_message(self, tcp_connection, buffer):
        """
        消息到来
        """
        raise NotImplementedError

    def write_complete(self):
        """
        消息发送完毕
        """
        raise NotImplementedError