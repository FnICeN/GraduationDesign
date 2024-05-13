import jieba
import pandas as pd
import numpy as np
from gensim import corpora, models
class VSM_tfidf:
    def __init__(self, rootpath : str, option_data):
        '''
        此类是VSM-tfidf算法，通过tf-idf对各词向量化并拼接以表示句向量，然后计算两个向量之间的余弦距离等来得出相似度
        rootpath: 项目地址
        option_data: 备选项数据，接受pd.DataFrame和list格式
        '''
        print("=================VSM_tfidf=================\n")
        self.option_data = option_data
        # 读取停用词
        self.stop_words = pd.read_csv(rootpath + "/GraduationDesign/语料库/stopwords.dat", delimiter="\t", header=None, quoting=3, encoding='utf-8')
        self.stop_words = self.stop_words[0].tolist()
        # 所有待选项分词处理，存入docs
        docs = []
        if type(option_data) == pd.DataFrame:
            print("接收到DataFrame类型")
            for doc in option_data.iloc[:,0]:
                temp_list = [word for word in jieba.cut(doc) if word not in self.stop_words and word !=' ']
                docs.append(temp_list)
        elif type(option_data) == list:
            print("接收到list类型")
            for doc in option_data:
                temp_list = [word for word in jieba.cut(doc) if word not in self.stop_words and word !=' ']
                docs.append(temp_list)
        else:
            print("VSM_tfidf接受的待匹配数据类型错误！只能是DataFrame或list类型！")
            return
        # 生成字典
        self.dictionary = corpora.Dictionary(docs)
        # 生成语料库
        self.option_corpus = [self.dictionary.doc2bow(doc) for doc in docs]
        # print('=================dictinary=============')
        # print('词ID到这个词在多少篇文档数的映射(dfs):',self.dictionary.dfs)
        # print('词到id编码的映射(token2id):',self.dictionary.token2id)
        # print('id编码到词的映射(id2token):',self.dictionary.id2token)
        # print('处理的文档数(num_docs):',self.dictionary.num_docs)
        # print('没有去重词条总数(num_pos):',self.dictionary.num_pos)
        # print('对文档内去重后的词条总数，文档间相同词不去重，只要记录BOW矩阵的非零元素个数(num_nnz):',self.dictionary.num_nnz)
        # print('=================dictinary=============')
        self.tfidf = models.TfidfModel(self.option_corpus)
    
    def getAnswerIndex(self, sample : str) -> list:
        '''
        根据sample从备选项中选出最相关的三项，返回一个元组列表[(similarity, index), ...]
        sample: 样本，即一个欲匹配的问题
        '''
        sample_list = [word for word in jieba.cut(sample) if word not in self.stop_words]
        sample_corpus = self.dictionary.doc2bow(sample_list)
        print("\n=================VSM_tfidf=================")
        return self.getProbAns(sample_corpus, self.option_corpus)

    def sim(self, option_corpus, test_tfidf, vocs):
        '''
        函数接收二维corpus[(bag_index, frequency), ...]和所有词列表vocs，返回两个corpus的相似度
        option_corpus: 某个备选项的corpus
        '''
        # corpus计算tfidf
        doc_tfidf = self.tfidf[option_corpus]
        # 将tfidf转换为字典形式，方便查找
        doc_tfidf_dict = {}
        test_tfidf_dict = {}
        for i in doc_tfidf:
            doc_tfidf_dict[i[0]] = i[1]
        for i in test_tfidf:
            test_tfidf_dict[i[0]] = i[1]
        # 创建向量
        vec_doc = []
        vec_test = []
        # 向量化
        for i in vocs:
            # 词在doc中的tfidf
            vec_doc.append(doc_tfidf_dict.get(i, 0))
            # 词在test中的tfidf
            vec_test.append(test_tfidf_dict.get(i, 0))
        # 计算余弦相似度
        return np.dot(vec_doc, vec_test) / (np.linalg.norm(vec_doc) * np.linalg.norm(vec_test))
    
    def getProbAns(self, sample_corpus, option_corpus):
        # 逐个比较，选出前三最相似者的相似度及索引
        res = []
        sample_tfidf = self.tfidf[sample_corpus]
        print("样本tfidf:", sample_tfidf)
        # 获取所有词
        vocs = set()
        for i in option_corpus:
            for j in i:
                vocs.add(j[0])
        for i in sample_corpus:
            vocs.add(i[0])
        vocs = list(vocs)
        
        for i in range(len(option_corpus)):
            res.append([self.sim(option_corpus[i], sample_tfidf, vocs), i])
        res.sort(reverse=True)
        return res[:3]    # (similarity, index)


# 读取客服数据
# df = pd.read_csv("E:/毕业设计/GraduationDesign/语料库/客服语料/整理后/1.csv")
# v = VSM_tfidf("E:/毕业设计", df)
# l = v.getAnswerIndex("我想更改我的账户密码，怎么办？")
# print(l)
# all_answer = df.iloc[:,1]
# print("匹配到问题：", df.iloc[l[0][1], 0])
# print("回答：", all_answer[l[0][1]])




