import pandas as pd
from utils.get_sentence_vec import GetSentenceVec
from random import randint
from torch.utils.data import Dataset
class TrainDataset(Dataset):
    def __init__(self, path, root_path):
        self.df = pd.read_csv(path)
        self.dflen = len(self.df)
        self.all_questions = []
        self.all_answers = []
        for doc in self.df.iloc[:,0]:
            self.all_questions.append(doc.strip())
        for doc in self.df.iloc[:,1]:
            self.all_answers.append(doc.strip())
        # 向量化
        q_v = GetSentenceVec(self.all_questions, root_path).get_sentences_vec(20)
        a_v = GetSentenceVec(self.all_answers, root_path).get_sentences_vec(20)
        self.all_questions = q_v
        self.all_answers = a_v
        # 生成负样本
        self.neg_answers = self.getNegSample(a_v)
        print("Dataloader问题集长度:{}，答案集长度:{}，负样本集长度:{}".format(len(self.all_questions), len(self.all_answers), len(self.neg_answers)))
    def __len__(self):
        return len(self.df)
    def __getitem__(self, idx):
        return self.all_questions[idx], self.all_answers[idx], self.neg_answers[idx]
    def getNegSample(self, a_v) -> list:
        neg_answers = []
        for i in range(len(a_v)):
            ridx = randint(0, len(a_v) - 1)
            while ridx == i:
                ridx = randint(0, len(a_v))
            neg_answers.append(a_v[ridx])
        return neg_answers
    
class PredictDataset(Dataset):
    def __init__(self, path, root_path):
        self.df = pd.read_csv(path)
        self.all_answers = []
        for doc in self.df.iloc[:,1]:
            self.all_answers.append(doc.strip())
        # 向量化，得到句向量列表，维度为(句子数量, 20, 200)
        self.a_v = GetSentenceVec(self.all_answers, root_path).get_sentences_vec(20)
    def __len__(self):
        return len(self.df)
    def __getitem__(self, idx):
        # 返回的是原句
        return self.all_answers[idx]
    
# dataset = MyDataset("D:\\GraduationDesign\\语料库\\客服语料\\整理后\\1.csv")
# dataloader = DataLoader(dataset, batch_size=10, shuffle=True, drop_last=True)
# for q, a, neg in dataloader:
#     print(q.shape)
#     print(a.shape)
#     print(neg.shape)
#     break