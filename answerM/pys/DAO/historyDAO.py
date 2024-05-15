from DAO.connPool import SqlPool
class historyDAOImpl:
    def __init__(self):
        self.sqlPool = SqlPool()
    def getUserAllHistory(self, userid : int):
        conn, cursor = self.sqlPool.getConn()
        sql = "select * from history where userid = %s"
        cursor.execute(sql, userid)
        print("userid:", userid)
        result = cursor.fetchall()
        self.sqlPool.closeConn(conn, cursor)
        return result
    def addHistory(self, userid, timestamp : str, q : str, a : str, llm : int):
        conn, cursor = self.sqlPool.getConn()
        sql = "insert into history(userid, timestamp, q, a, llm) values(%s, %s, %s, %s, %s)"
        cursor.execute(sql, (userid, timestamp, q, a, llm))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount
    def deleteHistoryByTimestamp(self, timestamp : str):
        conn, cursor = self.sqlPool.getConn()
        sql = "delete from history where timestamp = %s"
        cursor.execute(sql, (timestamp))
        conn.commit()
        self.sqlPool.closeConn(conn, cursor)
        return cursor.rowcount