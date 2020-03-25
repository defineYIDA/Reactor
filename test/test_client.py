# encoding=utf8

import tcp_client


class TestClient(tcp_client.TcpClient):
    def on_message(self, tcp_connection, buffer):
        print buffer.get_all()
        pass

    def write_complete(self):
        print 'client write done!'
        pass


def send(tcp_client):
    import time
    time.sleep(2)
    tcp_client.tcp_conn.send("........")


if __name__ == '__main__':
    import thread
    client = TestClient(10)
    client.connect(('127.0.0.1', 8080))
    thread.start_new_thread(send, (client,))
    client.run()
