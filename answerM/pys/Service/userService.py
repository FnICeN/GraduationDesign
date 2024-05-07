import sys
sys.path.append("..")
from DAO.userDAO import userDAOImpl
from DAO.ordersDAO import ordersDAOImpl
import json
sys.path.append("..")
from config import Config
class userServiceImpl:
    def __init__(self):
        self.userDAO = userDAOImpl()
        self.ordersDAO = ordersDAOImpl()
    def getUserNameById(self, userid):
        user = self.userDAO.getUserById(userid)
        if len(user) == 0:
            return None
        return user[0]["nickname"]
    def Login(self, username, password):
        user = self.userDAO.getUserLogin(username, password)
        succ = (len(user) == 1)
        if succ:
            res = {
            "success": succ,
            "data": {
                "username": f"{username}",
                "roles": ["admin"],
                "accessToken": "eyJhbGciOiJIUzUxMiJ9.admin",
                "refreshToken": "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
                "expires": "2030/10/30 00:00:00"
                }
            }
            # 登录成功，将userid存入config
            c = Config()
            c.userid = user[0]["userid"]
            c.username = user[0]["nickname"]
            return json.dumps(res)
        else:
            return json.dumps({"success" : succ, "data" : None})
    def addUser(self, nickname, password):
        res = self.userDAO.addUser(nickname, password)
        print("service完成")
        return res == 1
    def deleteUserById(self, userid):
        return self.userDAO.deleteUserById(userid)
    def getCurUserInfo(self):
        c = Config()
        userid = c.userid
        c.orderCount = self.ordersDAO.getUserAllOrdersCount(userid)
        details = self.ordersDAO.getOrdersByUserid(userid)
        sorCount = 0
        for detail in details:
            if detail["sta"] == "已下单" or detail["sta"] == "已发货":
                sorCount += 1
        c.sendOrReceiveCount = sorCount
        c.completeCount = len(details) - sorCount
        res = {
            "userid": c.userid,
            "username": c.username,
            "orderCount": c.orderCount,
            "sendOrReceiveCount": c.sendOrReceiveCount,
            "completeCount": c.completeCount
        }
        return json.dumps({"success": True, "data": res})
        
        
        
        