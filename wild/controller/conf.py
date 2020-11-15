# encoding=utf8


class Conf(object):
    """
    配置
    """
    CREAT_ROOM_WAIT_TIME = 3  # 创建房间等待时间
    ROOM_LIMIT = 8  # 房间人数上限

    # 消息枚举
    STATUS_REQ = "STATUS_REQ"  # 状态更改同步请求
    CREATE_REQ = "CREATE_REQ"  # 玩家创建请求
    SCENES_REQ = "SCENES_REQ"  # 场景创建成功

    BATTLE_REQ = "BATTLE_REQ"  # 战斗消息
    DEATH_REQ = "DEATH_REQ"  # 玩家死亡消息

    # 角色类型
    BOW = "BOW"  # 弓箭手
    WARRIOR = "WARRIOR"  # 战士
    MAGIC = "MAGIC"  # 法师

    #  游戏状态
    WAIT_JOIN = 0  # 等待房间创建阶段
    SCENE_LOAD = 1  # 场景加载成功阶段
    ALIVE = 2  # 战斗阶段
    DIE = 3  # 死亡（死亡后不退出就是自由视角）
    exit = 4  # 退出
