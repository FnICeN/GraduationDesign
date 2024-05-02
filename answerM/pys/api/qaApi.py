from flask import Blueprint, request
from Service.qaService import qaServiceImpl
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
    