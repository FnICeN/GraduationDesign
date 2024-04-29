import torch
from lstmModel import LSTMModel, evaluateModel, predict

class NetExecutor:
    def __init__(self, root_path, use_cuda : bool):
        self.rootpath = root_path
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
        lstm = LSTMModel(device = self.device, root_path = self.rootpath).to(self.device)
        # lstm.train("D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 128, 100)
        lstm.train()
        lstm.trainStart(data_path, batch_size, epoch, shuffle_neg)
    
    def LSTMEval(self, testdata_path : str, weight_path : str, batch_size : int):
        # 加载模型
        lstm = LSTMModel(self.device, self.rootpath).to(self.device)
        lstm.load_state_dict(torch.load(weight_path, map_location=self.device))
        print("加载模型成功")
        lstm.lstm.eval()
        evaluateModel(self.rootpath, lstm, self.device, testdata_path, batch_size)

    def LSTMPredict(self, question, ans_path, weight_path, GPTassis : bool):
        lstm = LSTMModel(self.device, self.rootpath).to(self.device)
        lstm.load_state_dict(torch.load(weight_path, map_location=self.device))
        print("加载模型成功")
        lstm.lstm.eval()
        predict(self.rootpath, question, ans_path, lstm, self.device, GPTassis)

# executor = NetExecutor("D:", False)
# executor.LSTMEval("D:/GraduationDesign/语料库/客服语料/整理后/7.csv", "D:/GraduationDesign/answerM/models/LSTMModel_weights.pth", 64)
# executor.LSTMPredict("我该如何修改我的账户密码？", "D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", "D:/GraduationDesign/answerM/models/0.1M-1layer/256b200e_shuffle/LSTMModel_weights.pth", True)
# executor.LSTMTrain("D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 64, 1, False)