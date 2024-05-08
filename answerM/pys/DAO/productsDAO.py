from DAO.connPool import SqlPool
class productsDAOImpl:
    def __init__(self):
        self.sqlPool = SqlPool()
    def getAllProducts(self):
        conn, cursor = self.sqlPool.getConn()
        sql = "select * from products"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def getProductById(self, productid):
        conn, cursor = self.sqlPool.getConn()
        sql = "select * from products where productid = %s"
        cursor.execute(sql, productid)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def addProduct(self, productname, price):
        conn, cursor = self.sqlPool.getConn()
        sql = "insert into products(productname, price) values(%s, %s)"
        cursor.execute(sql, (productname, price))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount
    def deleteProductById(self, productid):
        conn, cursor = self.sqlPool.getConn()
        sql = "delete from products where productid = %s"
        cursor.execute(sql, productid)
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount
    def updateProduct(self, productid, productname, price):
        conn, cursor = self.sqlPool.getConn()
        sql = "update products set productname = %s, price = %s where productid = %s"
        cursor.execute(sql, (productname, price, productid))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount