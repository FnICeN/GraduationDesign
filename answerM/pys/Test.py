from DAO.ordersDAO import ordersDAOImpl
import json
instance = ordersDAOImpl()
res = instance.getUserOrdersDetail(1)
print(res)