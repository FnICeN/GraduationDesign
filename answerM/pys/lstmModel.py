from random import randint
import torch
import torch.nn as nn

M = 0.1
class LSTMModel(nn.Module):
    def __init__(self, input_size = 200, hidden_size = 20, output_size = 200):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.hidden2out = nn.Linear(hidden_size, output_size)
    def forward(self, input):
        _, (hidden, _) = self.lstm(input)
        output = self.hidden2out(hidden)
        return output
    def train(self, q_data, ans_data, batch_size, epochs):
        optimizer = torch.optim.SGD(self.parameters(), lr=0.1)
        neg_data = self.getNegSample(ans_data)
        # 将data按照batch_size划分并训练epochs次
        for i in range(epochs):
            optimizer.zero_grad()
            for j in range(0, len(q_data), batch_size):
                q_input = q_data[j:j+batch_size]
                ans_input = ans_data[j:j+batch_size]
                neg_input = neg_data[j:j+batch_size]
                q_output = self(q_input)
                ans_output = self(ans_input)
                neg_output = self(neg_input)
                qa_sim = self.cal_cos(q_output, ans_output)
                qn_sim = self.cal_cos(q_output, neg_output)
                # qa_sim和qn_sim的差值越大越好，因此loss为M - (qa_sim - qn_sim)，M为一个常数
                loss = M - qn_sim - qa_sim
                loss.backward()
                optimizer.step()
                if i + 1 % 10 == 0:
                    print(f'Epoch { i + 1 }/{ epochs }, Loss: { loss.item() }')
    def getNegSample(self, ans_data) -> list:
        # 随机生成非问题回答的样本
        neg_sample = []
        for i in range(len(ans_data)):
            ridx = randint(0, len(ans_data))
            while ridx == i:
                ridx = randint(0, len(ans_data))
            neg_sample.append(ans_data[ridx])
        return neg_sample
    def cal_cos(v1 : torch.Tensor, v2 : torch.Tensor) -> torch.Tensor:
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
