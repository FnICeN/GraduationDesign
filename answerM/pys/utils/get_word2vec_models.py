import jieba
import pandas as pd
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence

class Processor:
    def __init__(self, root_path):
        self.rootpath = root_path
    def genModel(self, fileName):
        # 获取停用词
        stop_words = pd.read_csv(self.rootpath + "\\GraduationDesign\\语料库\\stopwords.dat", delimiter="\t", header=None, quoting=3, encoding='utf-8')
        stop_words = stop_words[0].tolist()

        df = pd.read_csv(self.rootpath + "\\GraduationDesign\\语料库\\客服语料\\整理后\\" + fileName + ".csv")

        # 生成问题的词向量模型
        q_list = []
        for doc in df.iloc[:,0]:
            q_list.append([word for word in jieba.cut(doc) if word not in stop_words and word !=' '])
        with open(self.rootpath + "\\GraduationDesign\\语料库\\q_vec.txt", "w", encoding="utf-8") as f:
            for q in q_list:
                f.write(" ".join(q) + "\n")
        model = word2vec.Word2Vec(LineSentence(self.rootpath + "\\GraduationDesign\\语料库\\q_vec.txt"), sg=0, vector_size=200, window=3, min_count=1, workers=8)
        model.save(self.rootpath + '\\GraduationDesign\\answerM\\models\\q_vec.model')

        # 生成答案的词向量模型
        a_list = []
        for doc in df.iloc[:,1]:
            a_list.append([word for word in jieba.cut(doc) if word not in stop_words and word !=' '])
        with open(self.rootpath + "\\GraduationDesign\\语料库\\a_vec.txt", "w", encoding="utf-8") as f:
            for a in a_list:
                f.write(" ".join(a) + "\n")
        model = word2vec.Word2Vec(LineSentence(self.rootpath + "\\GraduationDesign\\语料库\\a_vec.txt"), sg=0, vector_size=200, window=3, min_count=1, workers=8)
        model.save(self.rootpath + '\\GraduationDesign\\answerM\\models\\a_vec.model')

        # 生成问题和答案的词向量模型
        qa_list = q_list + a_list
        with open(self.rootpath + "\\GraduationDesign\\语料库\\qa_vec.txt", "w", encoding="utf-8") as f:
            for qa in qa_list:
                f.write(" ".join(qa) + "\n")
        model = word2vec.Word2Vec(LineSentence(self.rootpath + "\\GraduationDesign\\语料库\\qa_vec.txt"), sg=0, vector_size=200, window=3, min_count=1, workers=8)
        model.save(self.rootpath + '\\GraduationDesign\\answerM\\models\\qa_vec.model')
        print("模型生成完成")

processor = Processor("D:")
processor.genModel("[1-6]")