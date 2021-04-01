# encoding=utf8

if __name__ == '__main__':
    # 非法协议测试
    # telnet 127.0.0.1 8080
    # telnet可能是utf-8，1-3个字节表示一个字符
    # 写入超过4个字节后连接会被关闭
    pass