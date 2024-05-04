class Config:
    '''
    用于存储后端配置信息，以及当前登录用户的信息
    '''
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
        self.rootpath = ""
        self.answerFileName = ""
        # 使用模型的路径（以*rootpath*/GraduationDesign/answerM/models为根目录的相对路径）
        self.modelPath = ""
        Config._initialized = True
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance