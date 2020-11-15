# encoding=utf8
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]) + '/wild/wild')

if __name__ == '__main__':
    from wild_server import server_ins
    server_ins.heart_beat()
    server_ins.run()