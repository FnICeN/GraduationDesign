from flask import Blueprint, request
import json
import sys
sys.path.append("..")
from Service.ordersService import ordersServiceImpl

ordersApi = Blueprint("ordersApi", __name__)

@ordersApi.route('/getCurUserOrders', methods=['GET'])
def getUserOrders():
    osi = ordersServiceImpl()
    res = osi.curUserSendOrReceive()
    return json.dumps({"success" : True, "data" : res})

@ordersApi.route('/changeStatus', methods=['POST'])
def changeStatus():
    data = json.loads(request.get_data(as_text=True))
    osi = ordersServiceImpl()
    res = osi.changeCurUserOrderStatus(data['orderid'], data['status'])
    return json.dumps({"success" : res})