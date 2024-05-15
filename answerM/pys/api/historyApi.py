from flask import Blueprint, request
import json
import sys
sys.path.append("..")
from Service.historyService import historyServiceImpl

historyApi = Blueprint("historyApi", __name__)

@historyApi.route('/getCurUserHistory', methods=['GET'])
def getCurUserHistory():
    hs = historyServiceImpl()
    return json.dumps({"success" : True, "data" : hs.getCurUserHistory()})

@historyApi.route('/addHistory', methods=['POST'])
def addHistory():
    hs = historyServiceImpl()
    data = json.loads(request.get_data(as_text=True))
    return json.dumps({"success" : hs.addHistory(data["timestamp"], data["q"], data["a"], data["llm"])})

@historyApi.route('/deleteHistory', methods=['POST'])
def deleteHistory():
    hs = historyServiceImpl()
    data = json.loads(request.get_data(as_text=True))
    return json.dumps({"success" : hs.deleteHistory(data["timestamp"])})