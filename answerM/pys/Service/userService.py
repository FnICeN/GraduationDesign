import sys
sys.path.append("..")
from DAO.userDAO import userDAOImpl
import json
sys.path.append("..")
from config import Config
class userServiceImpl:
    def __init__(self):
        self.userDAO = userDAOImpl()
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
            return json.dumps(res)
        else:
            return json.dumps({"success" : succ, "data" : None})
    def addUser(self, username, password, nickname):
        self.userDAO.addUser(username, password, nickname)
    def deleteUserById(self, userid):
        return self.userDAO.deleteUserById(userid)