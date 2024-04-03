import numpy as np

from girth.synthetic import create_synthetic_irt_dichotomous
from girth import twopl_mml

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

