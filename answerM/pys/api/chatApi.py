from flask import Blueprint, request
import json
import pandas as pd
import sys
sys.path.append("..")
from BowAlgorithm import Bow
from BM25Algorithm import BM25
from VSM_tfidf_Algorithm import VSM_tfidf
from VSM_word2vec_Algorithm import VSM_word2vec
from LDemo import NetExecutor
from Service.userService import userServiceImpl
from Service.ordersService import ordersServiceImpl
from Service.productsService import productsServiceImpl
from utils.VecPersistence import SentenceVecPersis
from config import Config

class ChatModel():
    _initialed = False
    def __init__(self):
        # 只调用一次init
        if ChatModel._initialed:
            return
        print("ChatModel初始化...")
        self.model = None
        config = Config()
        self.df = pd.read_csv(f"{config.rootpath}/GraduationDesign/语料库/客服语料/整理后/{config.answerFileName}")
        self.all_answer = self.df.iloc[:,1]
        ChatModel._initialed = True
    def __new__(cls):
        # 单例模式
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
            print("ChatModel初次建立")
        return cls._instance
        
chatApi = Blueprint("chatApi", __name__)
@chatApi.route('/clear', methods=['GET'])
def clear():
    m = ChatModel()
    svp = SentenceVecPersis()
    m.model = None
    svp.a_v = None
    return json.dumps({"success" : True})

@chatApi.route('/changeMode', methods=['POST'])
def changeMode():
    print("changeMode")
    m = ChatModel()
    config = Config()
    # 获取请求数据
    data = json.loads(request.get_data(as_text=True))
    # 进行switch-case
    if data == 1:
        m.model = Bow(config.rootpath, m.df)
        return json.dumps({"success" : True})
    elif data == 2:
        m.model = BM25(config.rootpath, m.df)
        return json.dumps({"success" : True})
    elif data == 3:
        m.model = VSM_tfidf(config.rootpath, m.df)
        return json.dumps({"success" : True})
    elif data == 4:
        m.model = VSM_word2vec(config.rootpath, m.df, False)
        return json.dumps({"success" : True})
    elif data == 5:
        m.model = NetExecutor(config.rootpath, False)
        # 预先进行一次预测，以使得SentenceVecPersis类中的句向量持久化
        m.model.LSTMPredict("预先预测", 
                            f"{config.rootpath}/GraduationDesign/语料库/客服语料/整理后/{config.answerFileName}", 
                            f"{config.rootpath}/GraduationDesign/answerM/models/{config.modelPath}", 
                            False)
        return json.dumps({"success" : True})
    return json.dumps({"success" : False})

@chatApi.route('/getRes', methods=['POST'])
def getRes():
    usi = userServiceImpl()
    m = ChatModel()
    if m.model == None:
        return json.dumps({"success" : True, "data" : {"response" : "模型未初始化，请先选择匹配模式！"}})
    # 获取请求数据
    data = json.loads(request.get_data(as_text=True))
    # 进行switch-case
    if data["mode"] == 1:
        index = m.model.getProbAnsIndex(data["question"])
        answer = m.all_answer[index[0][0]]
        usi.userComplete()
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 2:
        _, max_index = m.model.getProbAnsIndex(data["question"])
        answer = m.all_answer[max_index[0]]
        usi.userComplete()
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 3:
        index = m.model.getAnswerIndex(data["question"])
        answer = m.all_answer[index[0][1]]
        usi.userComplete()
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 4:
        index = m.model.getProbAnsIndex(data["question"])
        answer = m.all_answer[index[0]]
        usi.userComplete()
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 5:
        config = Config()
        osi = ordersServiceImpl()
        psi = productsServiceImpl()
        usellm = data["usellm"]
        orders = None
        products = None
        if usellm:
            orders = osi.showCurUserAllOrders()
            products = psi.getAllProducts()
        res = m.model.LSTMPredict(data["question"], 
                            f"{config.rootpath}/GraduationDesign/语料库/客服语料/整理后/{config.answerFileName}", 
                            f"{config.rootpath}/GraduationDesign/answerM/models/{config.modelPath}", 
                            GPTassis = usellm, orders = orders, products = products)
        usi.userComplete()
        return json.dumps({"success" : True, "data" : {"response" : res}})
        
    return json.dumps({"success" : True, "data" : {"response" : "尚未配置该模式回复逻辑！"}})