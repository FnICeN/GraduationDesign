import pandas as pd
import sys
sys.path.append("..")
from DAO.qaDAO import qaDAOImpl
from config import Config

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
        self.config = Config()
        di = qaDataInfo()
        df = pd.DataFrame(self.qaDAO.getAllQA())
        # 去除df中的id列
        # df = df.drop(df.columns[0], axis=1)
        di.data = df
    def getQaLength(self):
        di = qaDataInfo()
        return di.data.shape[0]
    def getPageQa(self, page) -> list:
        limit = 15
        di = qaDataInfo()
        data = di.data[(int(page) - 1) * int(limit): (int(page) * int(limit))]
        return data.to_dict(orient='records')
    def addQa(self, q, a):
        return self.qaDAO.addQa(q, a, self.config.userid) == 1
    def deleteQaById(self, id):
        return self.qaDAO.deleteQaById(id) == 1
    def updateQaById(self, id, q, a):
        return self.qaDAO.updateQaById(id, q, a) == 1