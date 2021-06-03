## Reactor for python
python2.7 实现的网络框架，采用io多路复用的`reactor`模式。事件注册、分发的组织实现方式参考 netty 中`pipeline`。  

自定义协议，完善的拆解包流程，解决粘包半包，协议与框架分离，支持多协议的扩展。  
日志系统（辅助线程）、计时器（主线程）、handler线程安全（业务线程）等功能的实现。  

- [Select 唤醒的实现](https://github.com/defineYIDA/Reactor/issues/1)  

用于唤醒阻塞的io多路复用系统调用，不同平台的实现方式如下：  
> unix：self-pipe trick  
> win：a pair socket  

无论是通过`pipe`还是`socket`来实现，都是通过描述符的就绪事件来激活复用函数，往一个注册的描述符中写入一个字符来唤醒。  
那么对于水平触发(LE)的模型，一定得把这个字符给处理了，不然会一直处于就绪状态导致空轮询。

- 长连接管理  

应用层心跳 + 空闲检测  

定时器定时往所有客户端连接发送心跳包，同样客户端也定时发送心跳包到服务端，两端都通过心跳包的时间间隔判断连接是否失活，及时关闭失活连接。

- [handler线程安全](https://github.com/defineYIDA/Reactor/issues/2)  

`reactor`模式为单线程，所以就绪事件处理函数handler中如果有阻塞调用就会影响整个框架，对于阻塞操作正确的做法是在一个业务线程中执行。  
但是这样容易出现共享内存的线程安全问题，框架通过一个`event queue`将业务线程对函数的调用，延迟到主线程的`event loop`中。

***
## Event Dispatcher
事件分离采用的是责任链模式，如下：  

```
    def init_pipeline(self, pipe):
        pipe.set_proto_codec(MsgCodec())
        pipe.add_last(MsgDecodeHandler())
        pipe.add_last(EchoHandler())
        pipe.add_last(MsgEncodeHandler())
```
很方便注册处理事件handler到`pipeline`，接收到的字节流经过`pipeline`：  
`MsgDecodeHandler`进行解码 --> `EchoHandler`打印 --> `MsgEncodeHandler`编码发送到对端。

***
## Multi-protocol Extension

支持多协议，将协议和框架分离，实现上比较关键的是往框架注册协议的拆包器，用来判断一个完整的协议包是否就绪。  
```
        pipe.add_last(MsgSplitter())
```
对于未完整到达的协议包，直接在`pipeline`的`MsgSplitter`拆包器处就停止处理。

- 自定义协议  

msg 协议  
```
        自定义 msg 协议的编码
        +--------+----------+-------+--------+------------------+
        | 魔数   | 协议版本  |  指令 | 数据长度 |     数据         |
        +-------+----------+-------+--------+------------------+
         4byte     4byte    4byte    4byte       N byte
```
- 编解码器  

python自带模块——`struct` 来处理字节流。

- 拆包器  

基于长度字段的协议拆包器，通过数据长度字段在协议头部的偏移拿到数据长度，再通过数据长度判断完整的协议包体是否到达。

- [粘包和半包的处理](https://github.com/defineYIDA/NoneIM/issues/6)

每一个连接都对应着一个`buffer`，当连接可读事件就绪时，将数据存入`buffer`，并且用拆包器判断`buffer`中的数据是否满足一个完整的协议包体的要求，不满足直接停止处理等下一次就绪，否则从`buffer`中取出对应一个协议包长度的数据进行解码，进入`pipeline`进行后续处理。

***
## env
python: Python2.7  
platforms: win/linux  
无第三方包依赖
