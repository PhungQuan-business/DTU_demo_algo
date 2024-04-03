import torch
import numpy as np

def calculate_IFF(theta, alpha, beta):
    theta = theta.unsqueeze(1)
    argument = alpha * (theta - beta)
    P_i = 1 / (1 + torch.exp(-argument)).squeeze()

    Q_i =  1 - P_i
    information_gain = torch.square(alpha) * (P_i) * (Q_i)
    
    return information_gain
