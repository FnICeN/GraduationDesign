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
        admin = self.userDAO.getAdminLogin(username, password)
        succ = (len(user) == 1 or len(admin) == 1)
        if succ:
            roles = None
            c = Config()
            if len(admin) == 1:
                roles = ["admin"]
                c.userid = admin[0]["adminid"]
                c.username = admin[0]["name"]
                c.role = "admin"
                print("admin, id:", c.userid, "name:", c.username)
            else:
                roles = ["common"]
                c.userid = user[0]["userid"]
                c.username = user[0]["nickname"]
                c.role = "common"
                print("user, id:", c.userid, "name:", c.username)
            res = {
            "success": succ,
            "data": {
                "username": f"{username}",
                "roles": roles,
                "accessToken": "eyJhbGciOiJIUzUxMiJ9.admin",
                "refreshToken": "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
                "expires": "2030/10/30 00:00:00"
                }
            }
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
    
    def userComplete(self):
        c = Config()
        if c.role != "common":
            return
        userid = c.userid
        return self.userDAO.addUserCompleteNumber(userid) == 1
    def adminInsert(self):
        c = Config()
        if c.role != "admin":
            return
        adminid = c.userid
        return self.userDAO.addAdminInsertNumber(adminid) == 1
        
        
        
        