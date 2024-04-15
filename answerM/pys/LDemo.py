import torch
from lstmModel import LSTMModel, evaluateModel

class NetTrainExecutor:
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
        
    def LSTMTrain(self, data_path, batch_size, epoch):
        lstm = LSTMModel(device = self.device, root_path = self.rootpath).to(self.device)
        # lstm.train("D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 128, 100)
        lstm.train()
        lstm.trainStart(data_path, batch_size, epoch)
    
    def LSTMEval(self, rootpath : str, testdata_path : str, weight_path : str, batch_size : int):
        # 加载模型
        lstm = LSTMModel(self.device, rootpath)
        lstm.load_state_dict(torch.load(weight_path, map_location=self.device))
        lstm.eval()
        evaluateModel(rootpath, lstm, self.device, testdata_path, batch_size)

executor = NetTrainExecutor("D:", "D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 128, 100, False)
# executor = NetTrainExecutor("/root/autodl-tmp", True)
# executor.LSTMTrain("/root/autodl-tmp/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 128, 100)
executor.LSTMEval("D:", "D:/GraduationDesign/语料库/客服语料/整理后/7.csv", "D:/GraduationDesign/answerM/models/LSTMModel_weights.pth", 64)