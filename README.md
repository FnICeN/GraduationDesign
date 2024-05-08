# LSTM

文章原文是编写了embedding层，在调节层先maxpooling再tanh的，此时已实现降维；而本代码则是将max pooling改为了average pooling

实验发现，训练时需要取每个时间步的输出，求平均后计算loss再反向传播；而在预测时需要取最后一个时间步的输出，即直接input到model里面，通过自己写的forward得到结果

# GPT助选功能

由GPT回答问题，将GPT答案作为标准与三个备选答案对比，以相似度较高者作为GPT助选的答案。若相似度都很低，则直接使用GPT的答案作为回答

查询订单相关时，若GPT认为该问题与订单相关，则LSTM给出的回答必不正确，此时直接采用GPT的答案作为回答

相似度计算过程沿用四类已知的文本匹配算法，效果各有优劣。默认使用VSM-TFIDF算法

# 所有需要配置的文件

## 配置路径

- [answerM/pys/Server.py.example](answerM/pys/Server.py.example)

## 配置数据库

- [answerM/pys/test/ErroTest.ipynb](answerM/pys/test/ErroTest.ipynb)
- [answerM/pys/DAO/connPool.py.example](answerM/pys/DAO/connPool.py.example)

# 后续开发工作展望

