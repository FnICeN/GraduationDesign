import jieba
from gensim import corpora,models,similarities
import pandas as pd
class Bow:
    def __init__(self, rootpath : str, option_data):
        '''
        此类是Bow算法，通过tf-idf进行词嵌入，根据矩阵相似度从备选项中选出最相关的三项
        rootpath: 项目地址
        option_data: 备选项数据，接受pd.DataFrame和list格式
        '''
        print("=================Bow=================\n")
        self.option_data = option_data
        # 加载停用词
        self.stop_words = pd.read_csv(rootpath + "/GraduationDesign/语料库/stopwords.dat", delimiter="\t", header=None, quoting=3, encoding='utf-8')
        self.stop_words = self.stop_words[0].tolist()
        docs = []
        if type(option_data) == pd.DataFrame:
            for doc in option_data.iloc[:,0]:
                temp_list = [word for word in jieba.cut(doc) if word not in self.stop_words and word !=' ']
                docs.append(temp_list)
        elif type(option_data) == list:
            for doc in option_data:
                temp_list = [word for word in jieba.cut(doc) if word not in self.stop_words and word !=' ']
                docs.append(temp_list)
        # 生成词典
        self.dic = corpora.Dictionary(docs)
        # 生成语料库
        corpus = [self.dic.doc2bow(doc) for doc in docs]
        # 计算特征数、相似度索引（其实是得到一个字典，可以查到相似度）
        featureNum=len(self.dic.token2id.keys())
        self.index = similarities.SparseMatrixSimilarity(corpus, num_features=featureNum)
        
    def getProbAnsIndex(self, sample : str):
        '''
        根据sample从备选项中选出最相关的三项，返回一个元组列表[(index, similarity), ...]
        sample: 样本，即一个欲匹配的问题
        '''
        # 测试组分词，转词袋
        sample_doc = [word for word in jieba.cut(sample)]
        sample_corpus = self.dic.doc2bow(sample_doc)
        sim = self.index[sample_corpus]
        prob_index = sorted(enumerate(sim), key=lambda item: -item[1])[:3]
        print("\n=================Bow=================")
        return prob_index   # (index, similarity)


# df = pd.read_csv("E:/毕业设计/GraduationDesign/语料库/客服语料/整理后/1.csv")
# bow = Bow("E:/毕业设计", df)
# q = "如何账户密码？"
# index = bow.getProbAnsIndex(q)
# all_answer = df.iloc[:,1]
# print("问题：", q)
# print("匹配到问题：", df.iloc[index[0][0],0])
# print("回答：", all_answer[index[0][0]])

# 选择测试
# bow = Bow("D:", [
#     "您可以登录您的账户并前往“个人资料”页面更改您的密码。",
#     "对不起给您带来麻烦了，请您提供账户信息和异常活动详情。我们会尽快核实并采取相应措施，确保您的账户安全。同时，建议您加强账户密码管理和防范诈骗。",
#     "您可以在我们的网站上登录您的账户，然后进入“个人资料”页面，在那里您将有一个选项来更改您的密码。"
# ])
# prob_index = bow.getProbAnsIndex("要修改您的账户密码，请登录您的账户，然后导航到设置或账户管理页面。在那里，您应该能够找到一个选项来更改您的密码。请记得选择一个强密码，并确保您的新密码与以前的不同，以增强账户的安全性。如果您遇到任何问题，请查看平台的帮助中心或联系客服获取进一步的帮助。")
# print(prob_index)