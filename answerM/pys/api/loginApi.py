from flask import Blueprint, request
import json
from Service.userService import userServiceImpl

loginApi = Blueprint("loginApi", __name__)
@loginApi.route("/login", methods=['POST'])
def login():
    # 获取请求数据
    data = json.loads(request.get_data(as_text=True))
    usi = userServiceImpl()
    res = usi.Login(data["username"], data["password"])
    return res