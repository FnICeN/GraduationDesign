import jieba
import pandas as pd
import numpy as np
from gensim.models import word2vec
class VSM_word2vec:
    def __init__(self, rootpath : str, option_data, rebuild = True):
        '''
        此类是VSM-word2vec算法，通过word2vec对词向量化并求均值以表示句向量，然后计算两个向量之间的余弦距离等来得出相似度
        rootpath: 项目地址
        option_data: 备选项数据，接受pd.DataFrame和list格式
        rebuild: 是否重新训练模型，默认为True
        '''
        print("=================VSM_word2vec=================\n")
        # 读取停用词
        self.stop_words = pd.read_csv(rootpath + "/GraduationDesign/语料库/stopwords.dat", delimiter="\t", header=None, quoting=3, encoding='utf-8')
        self.stop_words = self.stop_words[0].tolist()
        self.docs = []
        if type(option_data) == pd.DataFrame:
            print("接收到DataFrame类型")
            for doc in option_data.iloc[:,0]:
                # 增加一步判断，若分词后为空，则不加入
                temp = [word for word in jieba.cut(doc) if word not in self.stop_words and word !=' ']
                if len(temp) > 0:
                    self.docs.append(temp)
        elif type(option_data) == list:
            print("接收到list类型")
            for doc in option_data:
                temp = [word for word in jieba.cut(doc) if word not in self.stop_words and word !=' ']
                if len(temp) > 0:
                    self.docs.append(temp)
        if rebuild:
            m = word2vec.Word2Vec(self.docs, sg=0, vector_size=200, window=3, min_count=1, workers=8)
            m.save(rootpath + '/GraduationDesign/answerM/models/word2vec.model')
        try:
            self.model = word2vec.Word2Vec.load(rootpath + '/GraduationDesign/answerM/models/word2vec.model')
        except:
            print("word2vec模型加载失败！")
            return
        self.dic = self.model.wv.index_to_key
        # 计算备选问题向量
        self.option_dict = {}
        for i, doc in enumerate(self.docs):
            doc_vec = []
            count = 0
            for word in doc:
                if word in self.dic:
                    doc_vec.append(self.model.wv[word])
            doc_vec = np.mean(doc_vec, axis=0)   # 求平均得句向量
            self.option_dict[i] = doc_vec

    def getProbAnsIndex(self, sample : str):
        '''
        根据sample从备选项中选出最相关的三项，返回一个列表[index, ...]
        sample: 样本，即一个欲匹配的问题
        '''
        # 计算问题向量
        sample = [word for word in jieba.cut(sample) if word not in self.stop_words and word !=' ']
        sample_vec = []
        for word in sample:
            if word in self.dic:
                sample_vec.append(self.model.wv[word])
        sample_vec = np.mean(sample_vec, axis=0)
        prob_ans = self.model.wv.cosine_similarities(sample_vec, [self.option_dict[i] for i in range(len(self.option_dict))])
        # 选出前三个最相似的
        prob_ans = np.argsort(prob_ans)[-3:]
        print("\n=================VSM_word2vec=================")
        return prob_ans.tolist()
    

# df = pd.read_csv("D:/GraduationDesign/语料库/客服语料/整理后/[1-6].csv")
# print(df.shape)
# v = VSM_word2vec("D:", df, True)
# prob_ans = v.getProbAnsIndex("怎么注册新帐号啊？")
# print(prob_ans)
# all_answer = df.iloc[:,1]
# print("匹配到问题：", df.iloc[prob_ans[0],0])
# print("回答：" + all_answer[prob_ans[0]])
# 选择测试
# v = VSM_word2vec("D:", [
#     "您可以登录您的账户并前往“个人资料”页面更改您的密码。",
#     "对不起给您带来麻烦了，请您提供账户信息和异常活动详情。我们会尽快核实并采取相应措施，确保您的账户安全。同时，建议您加强账户密码管理和防范诈骗。",
#     "您可以在我们的网站上登录您的账户，然后进入“个人资料”页面，在那里您将有一个选项来更改您的密码。"
# ])
# prob_index = v.getProbAnsIndex("要修改您的账户密码，请登录您的账户，然后导航到设置或账户管理页面。在那里，您应该能够找到一个选项来更改您的密码。请记得选择一个强密码，并确保您的新密码与以前的不同，以增强账户的安全性。如果您遇到任何问题，请查看平台的帮助中心或联系客服获取进一步的帮助。")
# print(prob_index)