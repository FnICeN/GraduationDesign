import torch.nn as nn
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.hidden2out = nn.Linear(hidden_size, output_size)
    def forward(self, input):
        _, (hidden, _) = self.lstm(input)
        output = self.hidden2out(hidden)
        return output
    
    
# input_size = 5
# hidden_size = 20
# output_size = 5
# model = LSTMModel(input_size, hidden_size, output_size)


# criterion = nn.CrossEntropyLoss()
# optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# epochs = 10
# for i in range(epochs):
#     optimizer.zero_grad()
#     input = torch.randn(3, 5)
#     output = model(input)
#     loss = criterion(output.squeeze(), torch.tensor([1, 2, 3, 4, 5]).float())
#     loss.backward()
#     optimizer.step()
#     print(f'Epoch { i + 1 }/{ epochs }, Loss: { loss.item() }')
