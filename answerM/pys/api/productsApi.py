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

@prodApi.route("/addProduct", methods=['POST'])
def addProduct():
    data = json.loads(request.get_data(as_text=True))
    psi = productsServiceImpl()
    res = psi.addProduct(data['productname'], data['price'])
    return json.dumps(res)

@prodApi.route("/deleteProduct", methods=['POST'])
def deleteProduct():
    data = json.loads(request.get_data(as_text=True))
    psi = productsServiceImpl()
    res = psi.deleteProductById(data['productid'])
    return json.dumps(res)

@prodApi.route("/updateProduct", methods=['POST'])
def updateProduct():
    data = json.loads(request.get_data(as_text=True))
    psi = productsServiceImpl()
    res = psi.updateProduct(data['productid'], data['productname'], data['price'])
    return json.dumps(res)
