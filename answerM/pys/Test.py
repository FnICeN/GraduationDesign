from DAO.qaDAO import qaDAOImpl
import pandas as pd
instance = qaDAOImpl()
# res = instance.addQa("q", "a")
res = instance.deleteQaById(5997)

print(res)