from flask import Flask, request
import json
import pandas as pd
from BowAlgorithm import Bow
from BM25Algorithm import BM25
from VSM_tfidf_Algorithm import VSM_tfidf
from VSM_word2vec_Algorithm import VSM_word2vec
from LDemo import NetExecutor

class Model:
    def __init__(self):
        self.model = None
        self.llm = None
# 创建应用实例
app = Flask(__name__)
# 视图函数（路由）
@app.route('/clear', methods=['GET'])
def clear():
    m.model = None
    return json.dumps({"success" : True})

@app.route('/changeMode', methods=['POST'])
def changeMode():
    # 获取请求数据
    data = json.loads(request.get_data(as_text=True))
    # 进行switch-case
    if data == 1:
        m.model = Bow("E:/毕业设计", df)
        return json.dumps({"success" : True})
    elif data == 2:
        m.model = BM25("E:/毕业设计", df)
        return json.dumps({"success" : True})
    elif data == 3:
        m.model = VSM_tfidf("E:/毕业设计", df)
        return json.dumps({"success" : True})
    elif data == 4:
        m.model = VSM_word2vec("E:/毕业设计", df, False)
        return json.dumps({"success" : True})
    elif data == 5:
        m.model = NetExecutor("E:/毕业设计", False)
        return json.dumps({"success" : True})
    return json.dumps({"success" : False})


@app.route('/getRes', methods=['POST'])
def getRes():
    if m.model == None:
        return json.dumps({"success" : True, "data" : {"response" : "模型未初始化，请先选择匹配模式！"}})
    # 获取请求数据
    data = json.loads(request.get_data(as_text=True))
    # 进行switch-case
    if data["mode"] == 1:
        index = m.model.getProbAnsIndex(data["question"])
        answer = all_answer[index[0][0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 2:
        _, max_index = m.model.getProbAnsIndex(data["question"])
        answer = all_answer[max_index[0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 3:
        index = m.model.getAnswerIndex(data["question"])
        answer = all_answer[index[0][1]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 4:
        index = m.model.getProbAnsIndex(data["question"])
        answer = all_answer[index[0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 5:
        res = m.model.LSTMPredict(data["question"], 
                            "E:/毕业设计/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 
                            "E:/毕业设计/GraduationDesign/answerM/models/0.1M-1layer/256b200e_shuffle/LSTMModel_weights.pth", 
                            data["usellm"])
        return json.dumps({"success" : True, "data" : {"response" : res}})
        
    return json.dumps({"success" : True, "data" : {"response" : "尚未配置该模式回复逻辑！"}})
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    df = pd.read_csv("E:/毕业设计/GraduationDesign/语料库/客服语料/整理后/[1-6].csv")
    all_answer = df.iloc[:,1]
    m = Model()
    app.run()