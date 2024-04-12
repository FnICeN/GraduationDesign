import torch
from torch import nn
from torch import Tensor
class Margin_Cosine_ReductionLoss(nn.Module):
    def __init__(self, margin : float):
        super(Margin_Cosine_ReductionLoss, self).__init__()
        self.margin = margin
    def forward(self, q : Tensor, a : Tensor, n : Tensor):
        '''
        要求q, a, n的shape为(batch_size, hidden_size)
        q: 问题向量
        a: 回答向量
        n: 负样本向量
        '''
        # 先各行向量点乘，得到行向量每个元素的平方，再在行上求和，得到每行的平方和，此时已变为一维向量，数量为batch_size
        # 然后对这个一维向量各元素开根号，得到原每行的模，即batch中每个sample句子的模长
        q_len = torch.sqrt(torch.sum(torch.mul(q, q), 1))
        a_len = torch.sqrt(torch.sum(torch.mul(a, a), 1))
        n_len = torch.sqrt(torch.sum(torch.mul(n, n), 1))
        # 求分子部分
        # 每行是两个不同类别sample各元素的乘积，一行中所有元素加起来即为两个sample的内积
        # 最终得到的也是一个一维向量，数量为batch_size，即batch中每两种sample的内积
        qa_dist = torch.sum(torch.mul(q, a), 1)
        qn_dist = torch.sum(torch.mul(q, n), 1)
        # 计算余弦相似度（得分），即两个向量的内积除以两个向量的模长之积，注意这里所有参与运算的变量都是一维向量
        qa_sim = torch.div(qa_dist, torch.mul(q_len, a_len))
        qn_sim = torch.div(qn_dist, torch.mul(q_len, n_len))
        # 定义margin和0
        margin = torch.full_like(qa_sim, self.margin)
        zero = torch.zeros_like(qa_sim)
        losses = torch.max(zero, torch.sub(margin, torch.sub(qa_sim, qn_sim)))
        return losses, torch.sum(losses)
