from itertools import count
from random import randint
import torch
import torch.nn as nn
import numpy as np
import trainRela.MyLoss as ml

M = 0.1
class LSTMModel(nn.Module):
    def __init__(self, input_size = 200, hidden_size = 200, output_size = 200):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.hidden2out = nn.Linear(hidden_size, output_size)
    def forward(self, input):
        _, (hidden, _) = self.lstm(input)
        output = self.hidden2out(hidden[-1])
        return output
    def train(self, q_data, ans_data, batch_size, epochs):
        # criterion = nn.CosineEmbeddingLoss(margin = M)
        criterion = ml.Margin_Cosine_ReductionLoss(M)
        optimizer = torch.optim.SGD(self.parameters(), lr=0.1)
        neg_data = self.getNegSample(ans_data)
        # 将data按照batch_size划分并训练epochs次
        for i in range(epochs):
            optimizer.zero_grad()
            acc_sum = 0
            for j in range(0, len(q_data), batch_size):
                q_input = np.array(q_data[j:j+batch_size])
                ans_input = np.array(ans_data[j:j+batch_size])
                neg_input = np.array(neg_data[j:j+batch_size])
                # 将输入转换为tensor
                q_input = torch.tensor(q_input).float()
                ans_input = torch.tensor(ans_input).float()
                neg_input = torch.tensor(neg_input).float()

                # print(q_input.shape)
                # 执行预测
                q_output, (_, _) = self.lstm(q_input)
                ans_output, (_, _) = self.lstm(ans_input)
                neg_output, (_, _) = self.lstm(neg_input)
                # print("q_output:", q_output.shape)
                # 在全连接层处理隐藏层输出
                q_output = self.hidden2out(q_output)
                ans_output = self.hidden2out(ans_output)
                neg_output = self.hidden2out(neg_output)
                # print(q_output.shape)
                # 将q_output由三维转为二维，(batch_size, hidden_size)或者可认为(batch_size, output_size)
                # 每个句子里的20个向量相加，求均值，得句向量
                q_output = torch.mean(q_output, dim=1)
                ans_output = torch.mean(ans_output, dim=1)
                neg_output = torch.mean(neg_output, dim=1)
                # print(q_output.shape)
                losses, loss = criterion(q_output, ans_output, neg_output)
                # 计算正确率
                acc_sum += self.getAccuracy(losses)
                loss.backward()
                optimizer.step()
            if (i + 1) % 10 == 0:
                print(f'Epoch { i + 1 }/{ epochs }, Loss: { loss.item() }')
                # 输出accuracy
                # print(f'Accuracy: { self.getAccuracy(correct, batch_size) }')
                print("以上10轮平均正确率:", acc_sum / 10)
    def getAccuracy(self, losses):
        # 计算正确率
        cor = torch.eq(torch.zeros_like(losses), losses)
        return torch.mean(cor.float(), dim=0)
        
    def getNegSample(self, ans_data) -> list:
        # 随机生成非问题回答的样本
        neg_sample = []
        for i in range(len(ans_data)):
            ridx = randint(0, len(ans_data) - 1)
            while ridx == i:
                ridx = randint(0, len(ans_data))
            neg_sample.append(ans_data[ridx])
        return neg_sample
    def cal_cos(self, v1 : torch.Tensor, v2 : torch.Tensor) -> torch.Tensor:
        # 余弦相似度，越大越不相似，完全一致时为0
        return 1 - torch.nn.functional.cosine_similarity(v1.squeeze(), v2.squeeze(), dim=0)

        
    
    
# input_size = 5
# hidden_size = 20
# output_size = 5
# model = LSTMModel(input_size, hidden_size, output_size)


# criterion = nn.CrossEntropyLoss()
# optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

# epochs = 10
# for i in range(epochs):
#     optimizer.zero_grad()
#     # 生成三行五列的整型随机数
#     input = torch.randint(0, 10, (3, 5)).float()
#     # input = torch.randn(3, 5)
#     print("input:\n", input)
#     output = model(input)
#     # loss = criterion(output.squeeze(), torch.tensor([1, 2, 3, 4, 5]).float())
#     # 损失定义为预测值和真实值的余弦相似度
#     print("output:\n", output)
#     loss = 1 - torch.nn.functional.cosine_similarity(output.squeeze(), torch.tensor([1, 2, 3, 4, 5]).float(), dim=0)
#     # 根据loss反向传播
#     loss.backward()
#     optimizer.step()
#     print(f'Epoch { i + 1 }/{ epochs }, Loss: { loss.item() }')

# print(torch.nn.functional.cosine_similarity(torch.tensor([0.1029, 0.4682, 0.4727, 0.6704, 0.8545]), torch.tensor([1, 2, 3, 4, 5]).float(), dim=0))
