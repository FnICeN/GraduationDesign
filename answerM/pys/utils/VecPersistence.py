class SentenceVecPersis:
    _initialized = False
    def __init__(self):
        if SentenceVecPersis._initialized:
            return
        print("句向量持久化类初始化...")
        self.a_v = None
        SentenceVecPersis._initialized = True
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
            print("句向量持久化类初次建立")
        return cls._instance