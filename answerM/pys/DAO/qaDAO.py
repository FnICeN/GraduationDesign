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