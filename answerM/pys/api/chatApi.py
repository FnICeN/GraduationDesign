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

class ChatModel():
    _initialed = False
    def __init__(self):
        # 只调用一次init
        if ChatModel._initialed:
            return
        print("ChatModel初始化...")
        self.model = None
        self.df = pd.read_csv("E:/毕业设计/GraduationDesign/语料库/客服语料/整理后/[1-6].csv")
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
    m.model = None
    return json.dumps({"success" : True})

@chatApi.route('/changeMode', methods=['POST'])
def changeMode():
    print("changeMode")
    m = ChatModel()
    # 获取请求数据
    data = json.loads(request.get_data(as_text=True))
    # 进行switch-case
    if data == 1:
        m.model = Bow("E:/毕业设计", m.df)
        return json.dumps({"success" : True})
    elif data == 2:
        m.model = BM25("E:/毕业设计", m.df)
        return json.dumps({"success" : True})
    elif data == 3:
        m.model = VSM_tfidf("E:/毕业设计", m.df)
        return json.dumps({"success" : True})
    elif data == 4:
        m.model = VSM_word2vec("E:/毕业设计", m.df, False)
        return json.dumps({"success" : True})
    elif data == 5:
        m.model = NetExecutor("E:/毕业设计", False)
        # 预先进行一次预测，以使得SentenceVecPersis类中的句向量持久化
        m.model.LSTMPredict("预先预测", 
                            "E:/毕业设计/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 
                            "E:/毕业设计/GraduationDesign/answerM/models/0.1M-1layer/256b200e_shuffle/LSTMModel_weights.pth", 
                            False)
        return json.dumps({"success" : True})
    return json.dumps({"success" : False})

@chatApi.route('/getRes', methods=['POST'])
def getRes():
    m = ChatModel()
    if m.model == None:
        return json.dumps({"success" : True, "data" : {"response" : "模型未初始化，请先选择匹配模式！"}})
    # 获取请求数据
    data = json.loads(request.get_data(as_text=True))
    # 进行switch-case
    if data["mode"] == 1:
        index = m.model.getProbAnsIndex(data["question"])
        answer = m.all_answer[index[0][0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 2:
        _, max_index = m.model.getProbAnsIndex(data["question"])
        answer = m.all_answer[max_index[0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 3:
        index = m.model.getAnswerIndex(data["question"])
        answer = m.all_answer[index[0][1]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 4:
        index = m.model.getProbAnsIndex(data["question"])
        answer = m.all_answer[index[0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 5:
        res = m.model.LSTMPredict(data["question"], 
                            "E:/毕业设计/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 
                            "E:/毕业设计/GraduationDesign/answerM/models/0.1M-1layer/256b200e_shuffle/LSTMModel_weights.pth", 
                            data["usellm"])
        return json.dumps({"success" : True, "data" : {"response" : res}})
        
    return json.dumps({"success" : True, "data" : {"response" : "尚未配置该模式回复逻辑！"}})