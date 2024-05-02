import pandas as pd
import sys
sys.path.append("..")
from DAO.qaDAO import qaDAOImpl

class qaDataInfo:
    _initialised = False
    def __init__(self):
        if qaDataInfo._initialised:
            return
        print("qaDataInfo初始化...")
        # 此data为DataFrame类型，方便去除id列以及做分页
        self.data: pd.DataFrame = None
        qaDataInfo._initialised = True
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
            print("qaDataInfo初次建立")
        return cls._instance

class qaServiceImpl:
    def __init__(self):
        self.qaDAO = qaDAOImpl()
        di = qaDataInfo()
        df = pd.DataFrame(self.qaDAO.getAllQA())
        # 去除df中的id列
        df = df.drop(df.columns[0], axis=1)
        di.data = df
    def getQaLength(self):
        di = qaDataInfo()
        return di.data.shape[0]
    def getPageQa(self, page) -> list:
        limit = 15
        di = qaDataInfo()
        data = di.data[(int(page) - 1) * int(limit): (int(page) * int(limit))]
        return data.to_dict(orient='records')