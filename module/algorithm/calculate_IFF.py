import torch
import numpy as np
from girth import twopl_mml
from girth import tag_missing_data, twopl_mml

def estimate_params(dataset):
    # Solve for parameters
    estimates = twopl_mml(dataset)
    """
        Returns:
        results_dictionary:
        * Discrimination: (1d array) estimate of item discriminations
        * Difficulty: (2d array) estimates of item diffiulties by item thresholds
        * LatentPDF: (object) contains information about the pdf
        * AIC: (dictionary) null model and final model AIC value
        * BIC: (dictionary) null model and final model BIC value
    """
    return estimates

def handling_null(dataset):
    # Assume its dichotomous data with True -> 1 and False -> 0
    tagged_data = tag_missing_data(dataset, [0, 1]).astype(int)
    
    return tagged_data

def calculate_IFF(dataset):
    # convert value to int for comaptibility with girth
    
    filled_dataset = handling_null(dataset)
    estimates = estimate_params(filled_dataset)

    alpha = torch.from_numpy(estimates['Discrimination'])
    beta = torch.from_numpy(estimates['Difficulty'])
    theta = torch.from_numpy(estimates['Ability'])

    theta = theta.unsqueeze(1)
    argument = alpha * (theta - beta)
    P_i = 1 / (1 + torch.exp(-argument)).squeeze()

    Q_i =  1 - P_i
    information_gain = torch.square(alpha) * (P_i) * (Q_i)
    
    return information_gain
