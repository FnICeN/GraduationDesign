import sys
sys.path.append("..")
from DAO.ordersDAO import ordersDAOImpl
from config import Config
class ordersServiceImpl:
    def __init__(self):
        self.ordersDAO = ordersDAOImpl()
    def curUserSendOrReceive(self):
        c = Config()
        userid = c.userid
        details = self.ordersDAO.getUserOrdersDetail(userid)
        res = []
        for detail in details:
            if detail["sta"] == "已下单" or detail["sta"] == "已发货":
                res.append(detail)
        return res
    def addOrder(self, productid):
        # 获取当前登录用户的userid
        c = Config()
        userid = c.userid
        orders = self.ordersDAO.getOrdersByUserid(userid)
        # 找到最大的orderid，新插入的orderid为最大orderid+1
        max_orderid = 0
        for order in orders:
            if order["orderid"] > max_orderid:
                max_orderid = order["orderid"]
        new_orderid = max_orderid + 1
        rowcount = self.ordersDAO.addOrder(userid, new_orderid, productid, "已下单")
        # 返回成功与否
        return rowcount > 0
    def deleteCurUserOrder(self, orderid):
        c = Config()
        userid = c.userid
        return self.ordersDAO.deleteOrderByUseridAndOrderid(userid, orderid) == 1
    def changeCurUserOrderStatus(self, orderid, status):
        c = Config()
        userid = c.userid
        return self.ordersDAO.updateOrderStatus(userid, orderid, status) == 1
    def showCurUserAllOrders(self):
        c = Config()
        userid = c.userid
        return self.ordersDAO.getUserOrdersDetail(userid)