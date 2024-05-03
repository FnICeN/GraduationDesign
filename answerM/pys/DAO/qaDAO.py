from DAO.connPool import SqlPool

class qaDAOImpl:
    def __init__(self):
        self.sqlPool = SqlPool()
    def getAllQA(self):
        conn, cursor = self.sqlPool.getConn()
        sql = "SELECT * FROM qa_data"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def addQa(self, q, a):
        conn, cursor = self.sqlPool.getConn()
        sql = "INSERT INTO qa_data (q, a) VALUES (%s, %s)"
        cursor.execute(sql, (q, a))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        # 返回受影响的行数
        return cursor.rowcount
    def deleteQaById(self, id):
        conn, cursor = self.sqlPool.getConn()
        sql = "DELETE FROM qa_data WHERE id = %s"
        cursor.execute(sql, id)
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount
    def updateQaById(self, id, q, a):
        conn, cursor = self.sqlPool.getConn()
        sql = "UPDATE qa_data SET q = %s, a = %s WHERE id = %s"
        cursor.execute(sql, (q, a, id))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount