from DAO.connPool import SqlPool
class userDAOImpl:
    def __init__(self):
        self.sqlPool = SqlPool()
    def getUserLogin(self, username, password):
        conn, cursor = self.sqlPool.getConn()
        sql = "select * from user where nickname = %s and password = %s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def getUserById(self, userid):
        conn, cursor = self.sqlPool.getConn()
        sql = "select * from user where userid = %s"
        cursor.execute(sql, userid)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def getAllUser(self):
        conn, cursor = self.sqlPool.getConn()
        sql = "select * from user"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def addUser(self, nickname, password):
        conn, cursor = self.sqlPool.getConn()
        sql = "insert into user(nickname, password) values(%s, %s)"
        cursor.execute(sql, (nickname, password))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount
    def deleteUserById(self, userid):
        conn, cursor = self.sqlPool.getConn()
        sql = "delete from user where userid = %s"
        cursor.execute(sql, userid)
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount