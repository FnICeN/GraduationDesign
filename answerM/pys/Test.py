from Service.ordersService import ordersServiceImpl
import json
instance = ordersServiceImpl()
# res = instance.addQa("q", "a")
res = instance.showCurUserAllOrders()
print(res)