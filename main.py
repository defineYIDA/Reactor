# encoding=utf8
import os
import sys
sys.path.append(sys.path[0] + '/wild/wild')

if __name__ == '__main__':
    # sys.path.append(os.path.dirname(sys.path[0]) + '\\test')
    print os.path.dirname(sys.path[0])
    # from test2.test2 import main1
    # main1()
    from wild_server import server_ins
    server_ins.heart_beat()
    server_ins.run()