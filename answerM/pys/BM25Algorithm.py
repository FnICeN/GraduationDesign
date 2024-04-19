import jieba
import numpy as np
import logging
import pandas as pd
from collections import Counter
jieba.setLogLevel(logging.INFO)

class BM25:
    def __init__(self, rootpath : str, option_data):
        '''
        此类是BM25算法，通过BM25特有的tf-idf计算方式进行词嵌入，再使用R算法计算词语得分，选出最相关的三项
        rootpath: 项目地址
        option_data: 备选项数据，接受pd.DataFrame和list格式
        '''
        print("=================BM25=================\n")
        # 参数设置
        self.k1 = 1.5
        self.b = 0.75
        self.option_data = option_data
        # 获取停用词
        self.stopwords = pd.read_csv(rootpath + "/GraduationDesign/语料库/stopwords.dat", delimiter="\t", header=None, quoting=3, encoding='utf-8')
        self.stopwords = self.stopwords[0].tolist()
        self.docs = []
        if type(option_data) == pd.DataFrame:
            print("接收到DataFrame类型")
            for doc in option_data.iloc[:,0]:
                temp_list = [word for word in jieba.cut(doc) if word not in self.stopwords and word !=' ']
                self.docs.append(temp_list)
        elif type(option_data) == list:
            print("接收到list类型")
            for doc in option_data:
                temp_list = [word for word in jieba.cut(doc) if word not in self.stopwords and word !=' ']
                self.docs.append(temp_list)
        self.vocab = set([word for doc in self.docs for word in doc]) # 文档中所包含的所有词语
        self.avgdl = sum([len(doc) + 0.0 for doc in self.docs]) / len(self.docs) # 所有文档的平均长度

    def getWordIdf(self, word):
        if word not in self.vocab:
            word_idf = 0
        else:
            # 统计包含该词语的文档数
            qn = {}
            for doc in self.docs:
                if word in doc:
                    if word in qn:
                        qn[word] += 1
                    else:
                        qn[word] = 1
                else:
                    continue
            word_idf = np.log((len(self.docs) - qn[word] + 0.5) / (qn[word] + 0.5))   #得到词语word的idf值（此idf为BM25的算法）
        return word_idf
    
    def getWordScoreList(self, word):
        # 计算词语word在各句的得分
        score_list = []
        wordIdf = self.getWordIdf(word)
        for doc in self.docs:   # 每句话
            word_count = Counter(doc)   # 统计一句话中各词语的词频
            if word in word_count.keys():   # 如果测试词语在这句话中
                f = (word_count[word]+0.0) / len(self.docs[0])
            else:
                f = 0.0
            r_score = (f * (self.k1 + 1)) / (f + self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl))   # 计算词语word的r_score
            score_list.append(wordIdf * r_score)    # 计算词语word在该句中的BM25分数
        return score_list
    
    def getSequenceScore(self, sequence):
        scores = []
        for word in sequence:
            scores.append(self.getWordScoreList(word))
        return np.sum(scores, axis=0)
    
    def getProbAnsIndex(self, sample : str):
        '''
        根据sample从备选项中选出最相关的三项，返回两个值, max_sim: [similarity, ...], max_index: [index, ...]
        sample: 样本，即一个欲匹配的问题
        '''
        # 问句处理
        sample = "我想更改我的账户密码，怎么办？"
        sample_list = [word for word in jieba.cut(sample) if word not in self.stopwords and word !=' ']
        sim = self.getSequenceScore(sample_list)
        sim = abs(sim)
        # 找到sim中最大的前3个值及其索引
        max_sim = []
        max_index = []
        for _ in range(3):
            max_sim.append(max(sim))
            max_index.append(np.argmax(sim))
            sim[np.argmax(sim)] = 0
        print("\n=================BM25=================")
        return max_sim, max_index

# 读取客服数据
# df = pd.read_csv("D:/GraduationDesign/语料库/客服语料/整理后/1.csv")
# bm = BM25("D:", df)
# max_sim, max_index = bm.getProbAnsIndex("我想更改我的账户密码，怎么办？")
# print("max_sim: {}\nmax_index: {}".format(max_sim, max_index))
# all_answer = df.iloc[:,1]
# print("匹配到问题：", df.iloc[max_index[0],0])
# print("回答：", all_answer[max_index[0]])

# 选择测试
# bm = BM25("D:", [
#     "您可以登录您的账户并前往“个人资料”页面更改您的密码。",
#     "对不起给您带来麻烦了，请您提供账户信息和异常活动详情。我们会尽快核实并采取相应措施，确保您的账户安全。同时，建议您加强账户密码管理和防范诈骗。",
#     "您可以在我们的网站上登录您的账户，然后进入“个人资料”页面，在那里您将有一个选项来更改您的密码。"
# ])
# max_sim, max_index = bm.getProbAnsIndex("要修改您的账户密码，请登录您的账户，然后导航到设置或账户管理页面。在那里，您应该能够找到一个选项来更改您的密码。请记得选择一个强密码，并确保您的新密码与以前的不同，以增强账户的安全性。如果您遇到任何问题，请查看平台的帮助中心或联系客服获取进一步的帮助。")
# print("max_sim: {}\nmax_index: {}".format(max_sim, max_index))