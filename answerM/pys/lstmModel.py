import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from utils.DataProcess import TrainDataset, PredictDataset
from utils.get_sentence_vec import GetSentenceVec
import trainRela.MyLoss as ml

M = 0.1
class LSTMModel(nn.Module):
    def __init__(self, device, root_path, input_size = 200, hidden_size = 200, output_size = 200, layers = 1):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=layers, batch_first=True)
        self.hidden2out = nn.Linear(hidden_size, output_size)
        self.device = device
        self.rootpath = root_path
        
    def forward(self, input):
        _, (hidden, _) = self.lstm(input)
        output = self.hidden2out(hidden[-1])
        return output
    def trainStart(self, data_path, batch_size, epochs, shuffle_neg):
        # 训练时取每个时间步的输出计算loss反向传播
        criterion = ml.Margin_Cosine_ReductionLoss(M)
        optimizer = torch.optim.SGD(self.parameters(), lr=0.1)
        dataset = TrainDataset(data_path, self.rootpath)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=True)
        print("本次训练参数：batchsize={}，epoch={}".format(batch_size, epochs))
        print("负样本打乱" if shuffle_neg else "负样本不打乱")
        # 将data按照batch_size划分并训练epochs次
        for i in range(epochs):
            acc_per_batch_record = []
            avg_acc_per_epoch_record = []
            for q_input, ans_input, neg_input in dataloader:
                optimizer.zero_grad()
                q_input = q_input.float()
                ans_input = ans_input.float()
                neg_input = neg_input.float()
                # 再次打乱neg_input
                if shuffle_neg:
                    neg_input = neg_input[torch.randperm(neg_input.size(0))]
                # 数据到device
                q_input = q_input.to(self.device)
                ans_input = ans_input.to(self.device)
                neg_input = neg_input.to(self.device)
                # 执行预测
                # q_output, (_, _) = self.lstm(q_input)
                # ans_output, (_, _) = self.lstm(ans_input)
                # neg_output, (_, _) = self.lstm(neg_input)
                q_output = self(q_input)
                ans_output = self(ans_input)
                neg_output = self(neg_input)
                # print("q_output:", q_output.shape)
                # 在全连接层处理隐藏层输出
                # q_output = self.hidden2out(q_output)
                # ans_output = self.hidden2out(ans_output)
                # neg_output = self.hidden2out(neg_output)
                # print(q_output.shape)
                # 将q_output由三维转为二维，(batch_size, hidden_size)或者可认为(batch_size, output_size)
                # 每个句子里的20个向量相加，求均值，得句向量
                # q_output = torch.mean(q_output, dim=1)
                # ans_output = torch.mean(ans_output, dim=1)
                # neg_output = torch.mean(neg_output, dim=1)
                # print(q_output.shape)
                losses, loss = criterion(q_output, ans_output, neg_output)
                # 计算正确率
                acc_per_batch_record.append(self.getAccuracy(losses))
                loss.backward()
                optimizer.step()
            avg_acc_per_epoch_record.append(sum(acc_per_batch_record) / len(acc_per_batch_record))
            if (i + 1) % 10 == 0:
                print(f'Epoch { i + 1 }/{ epochs }, Loss: { loss.item() }')
                # 输出accuracy
                # print(f'Accuracy: { self.getAccuracy(correct, batch_size) }')
                print("以上10轮平均正确率:", sum(avg_acc_per_epoch_record) / len(avg_acc_per_epoch_record))

        self.save_model("LSTMModel")
        print("训练结束，模型保存到{}/GraduationDesign/answerM/models/下".format(self.rootpath))
        

    def getAccuracy(self, losses):
        # 计算正确率
        cor = torch.eq(torch.zeros_like(losses), losses)
        return torch.mean(cor.float(), dim=0).item()
    
    def save_model(self, model_name : str):
        # 保存整个模型
        torch.save(self, self.rootpath + "/GraduationDesign/answerM/models/" + model_name + ".pth")
        # 保存模型参数
        torch.save(self.state_dict(), self.rootpath + "/GraduationDesign/answerM/models/" + model_name + "_weights.pth")
    

def evaluateModel(root_path : str, model : LSTMModel, device : torch.device, testdata_path : str, batch_size : int):
    criterion = ml.Margin_Cosine_ReductionLoss(M)
    # 加载测试数据
    dataset = TrainDataset(testdata_path, root_path)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=True)
    print("本次测试batchsize={}".format(batch_size))
    # 计算正确率
    acc_per_batch_record = []
    for q_input, ans_input, neg_input in dataloader:
        q_input = q_input.float()
        ans_input = ans_input.float()
        neg_input = neg_input.float()
        #是否使用GPU
        q_input = q_input.to(device)
        ans_input = ans_input.to(device)
        neg_input = neg_input.to(device)
        # 执行预测
        q_output = model(q_input)
        ans_output = model(ans_input)
        neg_output = model(neg_input)
        # 在全连接层处理隐藏层输出
        # q_output = model.hidden2out(q_output)
        # ans_output = model.hidden2out(ans_output)
        # neg_output = model.hidden2out(neg_output)
        # 将q_output由三维转为二维，(batch_size, hidden_size)或者可认为(batch_size, output_size)
        # 每个句子里的20个向量相加，求均值，得句向量
        # q_output = torch.mean(q_output, dim=1)
        # ans_output = torch.mean(ans_output, dim=1)
        # neg_output = torch.mean(neg_output, dim=1)
        losses, loss = criterion(q_output, ans_output, neg_output)
        # 计算正确率
        acc = model.getAccuracy(losses)
        acc_per_batch_record.append(acc)
        print("第{}批次正确率:{}".format(len(acc_per_batch_record), acc))
    print("测试完成，平均测试正确率:", sum(acc_per_batch_record) / len(acc_per_batch_record))

def predict(rootpath : str, question : str, ans_path : str, model : LSTMModel, device : torch.device, GPTassis : bool):
    '''
    根据问题预测答案
    return: 预测的三个备选答案
    '''
    # 预测时取最后一个时间步的输出作为结果
    # 加载答案数据
    ans_dataset = PredictDataset(ans_path, rootpath)
    # 处理问题
    question_vec = GetSentenceVec([question], rootpath).get_sentence_vec(20)
    question_vec = torch.tensor(question_vec).float().to(device)
    # 处理答案
    ans_vec = torch.tensor(ans_dataset.a_v).float().to(device)
    # 执行预测
    q_output = model(question_vec)
    ans_output = model(ans_vec)
    print("q_output:", q_output.shape)
    print("ans_output:", ans_output.shape)
    # 在全连接层处理隐藏层输出
    # q_output = model.hidden2out(q_output)
    # ans_output = model.hidden2out(ans_output)
    # 降维
    # q_output = torch.mean(q_output.squeeze(), dim = 0)
    # ans_output = torch.mean(ans_output, dim = 1)
    # 计算余弦相似度
    cos = nn.CosineSimilarity(dim = 1)
    sim_list = cos(q_output, ans_output)
    count_list = []
    for i in range(len(sim_list)):
        # 假设第i个是正确答案
        sub_list = torch.sub(torch.fill(sim_list, sim_list[i]), sim_list)
        # 统计与负向答案相似度之差大于0.5的个数
        count = torch.sum(torch.gt(sub_list, 0.5))
        count_list.append(count)
    max_idx_list = torch.argsort(torch.tensor(count_list))
    max_idx = max_idx_list[-1]
    sencond_idx = max_idx_list[-2]
    third_idx = max_idx_list[-3]
    dedi_ans = [ans_dataset.all_answers[max_idx], ans_dataset.all_answers[sencond_idx], ans_dataset.all_answers[third_idx]]
    print("问题:", question)
    print("答案一:", dedi_ans[0])
    print("答案二:", dedi_ans[1])
    print("答案三:", dedi_ans[2])
    return dedi_ans
    # # 取相似度最高的答案
    # max_index = torch.argmax(sim_list)
    # print("问题:", question)
    # print("答案:", ans_dataset.all_answers[max_index])
    


        # 使用wod2vec判断相似度
        # gptResVec = GetSentenceVec([gptRes], rootpath).get_sentence_vec(20)
        # gptResVec = torch.mean(torch.tensor(gptResVec).float(), dim = 0)
        # ans_vecs = torch.stack([ans_output[max_idx], ans_output[sencond_idx], ans_output[third_idx]])
        # sim_list = torch.abs(cos(gptResVec, ans_vecs))
        # print(sim_list)
        # max_idx = torch.argmax(sim_list)
        # if sim_list[max_idx] > 0.06:
        #     print("GPT辅助后回答:", dedi_ans[max_idx])
        # else:
        #     print("最终回答:", gptRes)










        
    
    
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
