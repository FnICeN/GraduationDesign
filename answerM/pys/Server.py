from flask import Flask

from api.loginApi import loginApi
from api.chatApi import chatApi
from api.productsApi import prodApi
from api.ordersApi import ordersApi

from config import Config

# 创建应用实例
app = Flask(__name__)

# 注册路由
app.register_blueprint(loginApi)
app.register_blueprint(chatApi)
app.register_blueprint(prodApi)
app.register_blueprint(ordersApi)

# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    c = Config()
    app.run()