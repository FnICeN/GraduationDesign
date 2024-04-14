import pandas as pd
import numpy as np
import utils.get_sentence_vec as gsv
from lstmModel import LSTMModel
# path = "D:"
# df = pd.read_csv(path + "\\GraduationDesign\\语料库\\客服语料\\整理后\\1.csv")
# all_questions = []
# all_answers = []
# for doc in df.iloc[:,0]:
#     all_questions.append(doc.strip())
# for doc in df.iloc[:,1]:
#     all_answers.append(doc.strip())
# q_v = gsv.GetSentenceVec(all_questions, 'D:\\GraduationDesign\\answerM\\models\\qa_vec.model').get_sentences_vec(20)
# a_v = gsv.GetSentenceVec(all_answers, 'D:\\GraduationDesign\\answerM\\models\\qa_vec.model').get_sentences_vec(20)
# print("shape of q_v:", q_v.shape)
# print("shape of a_v", a_v.shape)
lstm = LSTMModel()
lstm.train("D:\\GraduationDesign\\语料库\\客服语料\\整理后\\[1-6].csv", 128, 100)