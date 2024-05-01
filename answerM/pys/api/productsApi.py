from flask import Blueprint, request
import json
import sys
sys.path.append("..")
from Service.productsService import productsServiceImpl
from Service.ordersService import ordersServiceImpl

prodApi = Blueprint("prodApi", __name__)

@prodApi.route('/getAllProducts', methods=['GET'])
def getAllProducts():
    psi = productsServiceImpl()
    res = psi.getAllProducts()
    return json.dumps({"success" : True, "data" : res})

@prodApi.route('/buyProduct', methods=['POST'])
def buyProduct():
    data = json.loads(request.get_data(as_text=True))
    osi = ordersServiceImpl()
    res = osi.addOrder(data['productid'])
    return json.dumps({"success" : res})
