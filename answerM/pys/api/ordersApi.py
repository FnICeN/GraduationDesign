from flask import Blueprint, request
import json
import sys
sys.path.append("..")
from Service.ordersService import ordersServiceImpl

ordersApi = Blueprint("ordersApi", __name__)

@ordersApi.route("/getCurUserSendOrReceive", methods=['GET'])
def getCurUserSendOrReceive():
    osi = ordersServiceImpl()
    res = osi.curUserSendOrReceive()
    return json.dumps({"success" : True, "data" : res})

@ordersApi.route('/getCurUserAllOrders', methods=['GET'])
def getUserOrders():
    osi = ordersServiceImpl()
    res = osi.showCurUserAllOrders()
    return json.dumps({"success" : True, "data" : res})

@ordersApi.route('/changeStatus', methods=['POST'])
def changeStatus():
    data = json.loads(request.get_data(as_text=True))
    osi = ordersServiceImpl()
    res = osi.changeCurUserOrderStatus(data['orderid'], data['status'])
    return json.dumps({"success" : res})

@ordersApi.route('/deleteOrder', methods=['POST'])
def deleteOrder():
    data = json.loads(request.get_data(as_text=True))
    osi = ordersServiceImpl()
    res = osi.deleteCurUserOrder(data['orderid'])
    return json.dumps({"success" : res})