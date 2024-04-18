from openai import OpenAI
import json
import os

# os.environ["https_proxy"] = "https://proxy.fnicen.top/proxy/api.openai.com/v1/chat/completions"
# 设置代理
class GPTChat:
    def __init__(self, prompt : str):
        self.prompt = prompt
        self.client = OpenAI(
            api_key='sk-caDWGp0Ccg7ZULWLE7E799995f09484fBaAdB7012886B753',
            base_url="https://api.gpt.ge/v1/",
        )
    def getGPTResponse(self, ques_and_ans : dict) -> dict:
        resp = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": json.dumps(ques_and_ans)},
            ], 
        )
        return json.loads(resp.choices[0].message.content)
# res = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     response_format={ "type": "json_object" },
#     messages=[
#         {"role": "system", "content": "你是一个电商平台的智能客服答疑助手，你会收到JSON格式的消息，内容包括客户的疑问，以及三个可能的回答选项。你的输出是JSON格式，包含三个属性：三个选项当中最合适的回答most_prob_ans，但需要与用户的问题相关；自拟一个合理回答gen_ans；以及对于你做出这个选择的原因reason"},
#         {"role": "user", "content": '''{
#          question: "我该如何修改我的账户密码？",
#          ans_1: "我们接受信用卡、",
#          ans_2: "如果您在订购时遇到了付款问题，请尝试使用其他付款方式，例如信用卡、借记卡、PayPal等。如果仍然无法解决问题，请联系我们的客户服务部门以获取更多帮助。",
#          ans_3: "您好，请先确认您输入的支付信息是否正确。如果还是无法支付，请您联系银行或支付平台进行咨询。如果问题依然存在，您也可以联系我们的客服人员协助您解决。",
#         }'''},
#     ], 
# )
# gpt = GPTChat("你是一个电商平台的智能客服答疑助手，你会收到JSON格式的消息，内容包括客户的疑问，以及三个可能的回答选项。你的输出是JSON格式，包含两个属性：三个选项当中最合适的回答most_prob_ans，但需要与用户的问题相关，若不相关或未回答该问题，则用null填充本属性；自拟一个合理回答gen_ans")
# gpt = GPTChat("你是一个电商平台的智能客服答疑助手，你会收到JSON格式的消息，内容包括客户的疑问question，以及三个可能的回答选项ans_1-3。你的输出是JSON格式，包含属性：自拟一个合理回答gen_ans")

# res = gpt.getGPTResponse({
#     "question": "你们支持哪些支付方式？",
#     "ans_1": "我们接受信用卡、",
#     "ans_2": "如果您在订购时遇到了付款问题，请尝试使用其他付款方式，例如信用卡、借记卡、PayPal等。如果仍然无法解决问题，请联系我们的客户服务部门以获取更多帮助。",
#     "ans_3": "您好，请先确认您输入的支付信息是否正确。如果还是无法支付，请您联系银行或支付平台进行咨询。如果问题依然存在，您也可以联系我们的客服人员协助您解决。",
# })
# print(res)