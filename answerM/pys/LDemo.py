import torch
from lstmModel import LSTMModel

class NetTrainExecutor:
    def __init__(self, root_path, data_path, batch_size, epoch):
        self.rootpath = root_path
        self.data_path = data_path
        self.batch_size = batch_size
        self.epoch = epoch
        
    def LSTMTrain(self, use_cuda : bool):
        device = None
        if use_cuda == True:
            if torch.cuda.is_available() == True:
                print("显卡模式")
                device = torch.device('cuda')
            else:
                print("选择显卡模式，但无显卡，切换到cpu模式")
                device = torch.device('cpu')
        else:
            print("cpu模式")
            device = torch.device('cpu')
        lstm = LSTMModel(device=device, root_path = self.rootpath).to(device)
        # lstm.train("D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 128, 100)
        lstm.train(self.data_path, self.batch_size, self.epoch)

executor = NetTrainExecutor("D:", "D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 128, 100)
# executor = NetTrainExecutor("/root/autodl-tmp", "/root/autodl-tmp/GraduationDesign/语料库/客服语料/整理后/[1-6].csv", 128, 100)
executor.LSTMTrain(False)