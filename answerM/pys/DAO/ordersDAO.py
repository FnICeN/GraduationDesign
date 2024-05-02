from DAO.connPool import SqlPool
class ordersDAOImpl:
    def __init__(self):
        self.sqlPool = SqlPool()
    def getAllOrders(self):
        conn, cursor = self.sqlPool.getConn()
        sql = "select * from orders"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def getUserAllOrdersCount(self, userid):
        conn, cursor = self.sqlPool.getConn()
        sql = "select count(*) from orders where userid = %s"
        cursor.execute(sql, userid)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        # 返回数字
        return result[0]["count(*)"]
    def getOrdersByUserid(self, userid):
        conn, cursor = self.sqlPool.getConn()
        sql = "select * from orders where userid = %s"
        cursor.execute(sql, userid)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        # 若无订单则返回长度为0的元组
        return result
    def getUserOrdersDetail(self, userid):
        conn, cursor = self.sqlPool.getConn()
        sql = "select orderid,productname,price,sta from orders, products where orders.productid=products.productid and userid=%s;"
        cursor.execute(sql, userid)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def addOrder(self, userid, orderid, productid, status):
        conn, cursor = self.sqlPool.getConn()
        sql = "insert into orders(userid, orderid, productid, sta) values(%s, %s, %s, %s)"
        cursor.execute(sql, (userid, orderid, productid, status))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        # 返回受影响的行数
        return cursor.rowcount
    def deleteOrderByUseridAndOrderid(self, userid, orderid):
        conn, cursor = self.sqlPool.getConn()
        sql = "delete from orders where userid = %s and orderid = %s"
        cursor.execute(sql, (userid, orderid))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        # 返回受影响的行数
        return cursor.rowcount
    def updateOrderStatus(self, userid, orderid, status):
        conn, cursor = self.sqlPool.getConn()
        sql = "update orders set sta = %s where userid = %s and orderid = %s"
        cursor.execute(sql, (status, userid, orderid))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        # 返回受影响的行数
        return cursor.rowcount
        