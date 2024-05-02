class Config:
    _initialized = False
    def __init__(self):
        if Config._initialized:
            return
        # 用于存储当前登录用户的userid
        print("config被初始化")
        self.username = "未登录"
        self.orderCount = 0
        self.sendOrReceiveCount = 0
        self.completeCount = 0
        self.userid = 0
        Config._initialized = True
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance