# encoding=utf8

if __name__ == '__main__':
    import room_queue, time, room_manager

    room_queue.room_queue.add_wait("111")

    room_queue.room_queue.add_wait("222")

    room_queue.room_queue.add_wait("333")

    room_queue.room_queue.add_wait("444")

    room_queue.room_queue.add_wait("555")

    print room_manager.room_manager.room_map
    time.sleep(10)
    print room_manager.room_manager.room_map
