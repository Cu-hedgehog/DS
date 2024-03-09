import numpy as np
import torch
from torch import nn

def create_model():
    import torch
    from torch import nn
    model = nn.Sequential(
        nn.Linear(784, 256, True),
        nn.ReLU(),
        nn.Linear(256, 16, True),
        nn.ReLU(),
        nn.Linear(16, 10, True),
        nn.ReLU())
    
    return model

model = create_model()

def count_parameters(model):
    import torch
    from torch import nn
    result = 0
    n = len(list(model.parameters()))
    for i in range(n):
        layer_result = 1
        m = len(list(model.parameters())[i].size())
        for j in range(m):
            layer_result *= list(model.parameters())[i].size()[j]
        result += layer_result
    return result

count_parameters(model)
    