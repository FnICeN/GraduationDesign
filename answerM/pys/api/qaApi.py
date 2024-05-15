from flask import Blueprint, request
from Service.qaService import qaServiceImpl
from Service.userService import userServiceImpl
import json

qaApi = Blueprint("qaApi", __name__)



@qaApi.route('/getQaLength', methods=['GET'])
def getQaLength():
    qsi = qaServiceImpl()
    length = qsi.getQaLength()
    return json.dumps(length)

@qaApi.route('/getQa', methods=['POST'])
def getQa():
    page = json.loads(request.get_data(as_text=True))
    qsi = qaServiceImpl()
    data = qsi.getPageQa(page)
    return json.dumps({"page": page, "data": data})

@qaApi.route('/addQa', methods=['POST'])
def addQa():
    data = json.loads(request.get_data(as_text=True))
    qsi = qaServiceImpl()
    usi = userServiceImpl()
    res = qsi.addQa(data['q'], data['a'])
    if res:
        usi.adminInsert()
    return json.dumps({"success": res})

@qaApi.route('/delQa', methods=['POST'])
def deleteQa():
    data = json.loads(request.get_data(as_text=True))
    qsi = qaServiceImpl()
    res = qsi.deleteQaById(data['id'])
    return json.dumps({"success": res})

@qaApi.route('/updateQa', methods=['POST'])
def updateQa():
    data = json.loads(request.get_data(as_text=True))
    qsi = qaServiceImpl()
    res = qsi.updateQaById(data['id'], data['q'], data['a'])
    return json.dumps({"success": res})
    