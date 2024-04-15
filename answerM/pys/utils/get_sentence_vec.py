import jieba
import pandas as pd
import numpy as np
from gensim.models import word2vec


class GetSentenceVec:
    '''
    通过word2vec模型获取句子向量，无需提前分词，直接传入句子即可
    data: 待处理的数据（列表形式）
    model_path: word2vec模型路径
    '''
    def __init__(self, data : list, root_path):
        self.data = data
        self.rootpath = root_path
        self.model = word2vec.Word2Vec.load(root_path + "/GraduationDesign/answerM/models/qa_vec.model")
    
    def pad_sentence(self, tokenized_sentence, seq_length, default_dim = 200):
        '''
        将句子填充到指定长度
        tokenized_sentence: 分词后的句子
        seq_length: 填充长度
        default_dim: 默认填充向量维度，默认为200
        '''
        # 考虑到有些句子中没有有效词，但若不将本句话加入结果中，会导致答案与问题不对应，所以考虑用全0填充
        if len(tokenized_sentence) == 0:
            return [[0] * default_dim] * seq_length
        sentence = []
        if len(tokenized_sentence) >= seq_length:
            sentence = tokenized_sentence[:seq_length]
        else:
            sentence = tokenized_sentence + [[0] * len(tokenized_sentence[0])] * (seq_length - len(tokenized_sentence))
        return sentence

    def cut_to_words(self):
        # 获取停用词
        stop_words = pd.read_csv(self.rootpath + "/GraduationDesign/语料库/stopwords.dat", delimiter="\t", header=None, quoting=3, encoding='utf-8')
        stop_words = stop_words[0].tolist()
        # 若是多个句子，则返回嵌套列表
        if len(self.data) > 1:
            res = []
            for sentence in self.data:
                res.append([word for word in jieba.cut(sentence) if word not in stop_words and word !=' '])
            return res
        # 单个句子返回列表
        return [word for word in jieba.cut(self.data[0]) if word not in stop_words and word !=' ']
    
    
    def get_sentences_vec(self, pad_length):
        '''
        一次性计算所有句子中词的向量
        pad_length: 填充长度
        '''
        words = self.cut_to_words()
        res = []
        for sentence in words:
            sentence_vec = []
            for word in sentence:
                try:
                    sentence_vec.append(self.model.wv[word])
                except:
                    pass
            sentence_vec = self.pad_sentence(sentence_vec, pad_length)
            res.append(sentence_vec)
        return np.array(res)
    
    def get_sentence_vec(self, pad_length):
        '''
        计算一个句子中词的向量
        pad_length: 填充长度
        '''
        words = self.cut_to_words()
        res = []
        for word in words:
            try:
                res.append(self.model.wv[word])
            except:
                pass
        res = self.pad_sentence(res, pad_length)
        return np.array(res)
            

    