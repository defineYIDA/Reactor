# encoding=utf8

import tcp_client
import message_packet


class TestClient(tcp_client.TcpClient):
    def on_message(self, tcp_connection, command, packet):
        print packet.get_command()
        print packet.get_message()

    def write_complete(self):
        print 'client write done!'
        pass


def send(tcp_client):
    import time
    time.sleep(2)
    msg = message_packet.MessagePacket("hello!!!")
    tcp_client.send(msg)


if __name__ == '__main__':
    import thread
    client = TestClient(10)
    client.connect(('127.0.0.1', 8080))
    thread.start_new_thread(send, (client,))
    client.run()
