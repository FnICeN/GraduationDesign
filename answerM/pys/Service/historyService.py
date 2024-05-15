import sys
sys.path.append("..")
from DAO.historyDAO import historyDAOImpl
from config import Config
class historyServiceImpl:
    def __init__(self):
        self.historyDAO = historyDAOImpl()
        self.config = Config()
    def addHistory(self, timestamp : str, q : str, a : str, llm : int) -> bool:
        if self.config.role == "admin":
            return
        return self.historyDAO.addHistory(self.config.userid, timestamp, q, a, llm) == 1
    def getCurUserHistory(self):
        return self.historyDAO.getUserAllHistory(self.config.userid)
    def deleteHistory(self, timestamp : str) -> bool:
        return self.historyDAO.deleteHistoryByTimestamp(timestamp) == 1