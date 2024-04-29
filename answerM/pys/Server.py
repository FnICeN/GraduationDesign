from flask import Flask, request
import json
import pandas as pd
from BowAlgorithm import Bow
from BM25Algorithm import BM25
from VSM_tfidf_Algorithm import VSM_tfidf
from VSM_word2vec_Algorithm import VSM_word2vec
from LDemo import NetExecutor

df = pd.read_csv("E:/毕业设计/GraduationDesign/语料库/客服语料/整理后/[1-6].csv")
all_answer = df.iloc[:,1]
# 创建应用实例
app = Flask(__name__)
# 视图函数（路由）
@app.route('/getRes', methods=['POST'])
def getRes():
    # 获取请求数据
    data = json.loads(request.get_data(as_text=True))
    # 进行switch-case
    if data["mode"] == 1:
        bow = Bow("E:/毕业设计", df)
        index = bow.getProbAnsIndex(data["question"])
        answer = all_answer[index[0][0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 2:
        bm25 = BM25("E:/毕业设计", df)
        _, max_index = bm25.getProbAnsIndex(data["question"])
        answer = all_answer[max_index[0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 3:
        vsm_tfidf = VSM_tfidf("E:/毕业设计", df)
        index = vsm_tfidf.getAnswerIndex(data["question"])
        answer = all_answer[index[0][1]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
    
    elif data["mode"] == 4:
        vsm_word2vec = VSM_word2vec("E:/毕业设计", df, False)
        index = vsm_word2vec.getProbAnsIndex(data["question"])
        answer = all_answer[index[0]]
        return json.dumps({"success" : True, "data" : {"response" : answer}})
        
    return json.dumps({"success" : True, "data" : {"response" : "尚未配置该模式回复逻辑！"}})
# 启动实施（只在当前模块运行）
if __name__ == '__main__':
	app.run()