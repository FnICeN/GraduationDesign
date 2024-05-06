import torch
from lstmModel import LSTMModel, evaluateModel, predict
from LLMRela.ChatGPTDemo import GPTChat
from VSM_tfidf_Algorithm import VSM_tfidf
import json

GPT_M = 0.4
class NetExecutor:
    def __init__(self, root_path, use_cuda : bool):
        self.rootpath = root_path
        # 为了保证每次调用LSTMPredict时用的是同一个GPTChat实例
        self.gpt = None
        if use_cuda == True:
            if torch.cuda.is_available() == True:
                print("显卡模式")
                self.device = torch.device('cuda')
            else:
                print("选择显卡模式，但无显卡，切换到cpu模式")
                self.device = torch.device('cpu')
        else:
            print("cpu模式")
            self.device = torch.device('cpu')
        
    def LSTMTrain(self, data_path, batch_size, epoch, shuffle_neg : bool):
        lstm = LSTMModel(device = self.device, root_path = self.rootpath, layers=1).to(self.device)
        # lstm.train("D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 128, 100)
        lstm.train()
        lstm.trainStart(data_path, batch_size, epoch, shuffle_neg)
    
    def LSTMEval(self, testdata_path : str, weight_path : str, batch_size : int):
        # 加载模型
        lstm = LSTMModel(self.device, self.rootpath, layers=1).to(self.device)
        lstm.load_state_dict(torch.load(weight_path, map_location=self.device))
        print("加载模型成功")
        lstm.eval()
        evaluateModel(self.rootpath, lstm, self.device, testdata_path, batch_size)

    def LSTMPredict(self, question, ans_path, weight_path, GPTassis : bool, orders : list = None, products : list = None):
        lstm = LSTMModel(self.device, self.rootpath, layers=1).to(self.device)
        lstm.load_state_dict(torch.load(weight_path, map_location=self.device))
        print("加载模型成功")
        lstm.eval()
        dedi_ans = predict(self.rootpath, question, ans_path, lstm, self.device, GPTassis)
        final_ans = dedi_ans[0]
        if GPTassis:
            for i in range(5):
                try:
                    if self.gpt == None:
                        self.gpt = GPTChat("""
                                    你是一个电商平台客服，你会收到JSON格式的消息，消息格式为：
                                    {
                                        'question' : '用户的问题',
                                        'orders' : 
                                            [
                                                {
                                                'orderid' : '订单号',
                                                'productname' : '产品名称',
                                                'price' : '价格',
                                                'sta' : '状态',
                                                },
                                                ...
                                            ]
                                        'products' : 
                                           [
                                                {
                                                'productid' : '产品编号',
                                                'productname' : '产品名称',
                                                'price' : '价格',
                                                },
                                                ...
                                           ]
                                        }
                                        你需要根据用户的问题，必要时可以参考用户的订单信息或系统中已有的商品信息，回答用户的问题，回答尽量简洁一些。
                                        你需要输出JSON格式的消息，为：
                                        {
                                            'gen_ans' : '你的回答'
                                            'aboutOrderOrRecommend' : 问题是否是关于用户订单的问题或关于向用户推荐商品的问题，是则为true，否则为false
                                        }
                                        """)
                    gptRes = self.gpt.getGPTSeveralResponses(
                        {
                            "question": question,
                            "orders": orders,
                            "products": products
                        }
                    )
                    break
                except:
                    if i != 4:
                        print("GPT请求失败，重试（第{}次）...".format(i + 1))
                    else:
                        print("GPT请求失败，重试5次仍失败，退出")
                        return
            gptRes_text = gptRes["gen_ans"]
            gptRes_choose = gptRes["aboutOrderOrRecommend"]
            # gptRes_text有概率为unicode编码，需要转换
            print("gptRes的类型：", type(gptRes_text), "gptRes的值：", gptRes_text)
            gptRes_text = json.loads('"' + gptRes_text + '"', strict=False)
            print("GPT辅助回答:", gptRes_text)
            if gptRes_choose == True:
                print("GPT认为问题是关于订单或推荐的问题，直接使用GPT回答")
                final_ans = gptRes_text
                return final_ans
            # 使用VSM-tfidf判断相似度
            vsm = VSM_tfidf(self.rootpath, dedi_ans)
            prob_index = vsm.getAnswerIndex(gptRes_text)
            
            print(prob_index)
            if prob_index[0][0] > GPT_M:
                final_ans = dedi_ans[prob_index[0][1]]
                print("GPT助选，选择合理答案")
            else:
                final_ans = gptRes_text
                print("GPT认为不存在合理答案，使用自拟答案")
            print("最终回答：", final_ans)
        return final_ans

# executor = NetExecutor("D:", False)
# executor.LSTMEval("D:/GraduationDesign/语料库/客服语料/整理后/7.csv", "D:/GraduationDesign/answerM/models/LSTMModel_weights.pth", 64)
# executor.LSTMPredict("我该如何修改我的账户密码？", "D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", "D:/GraduationDesign/answerM/models/0.1M-1layer/256b200e_shuffle/LSTMModel_weights.pth", True)
# executor.LSTMTrain("D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 64, 1, False)