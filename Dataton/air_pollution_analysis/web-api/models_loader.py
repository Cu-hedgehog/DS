import pickle
import json
#import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import sklearn

def load_models(paths: dict) -> dict:
    res ={}
    res['knn'] = pickle.load(open(paths['knn'], 'rb'))
    res['boosting'] =  pickle.load(open(paths['boosting'], 'rb'))
    res['forest'] = pickle.load(open(paths['forest'], 'rb'))
    res['lasso'] = pickle.load(open(paths['lasso'], 'rb'))
    res['linear'] =  pickle.load(open(paths['linear'], 'rb'))
    res['svr'] = pickle.load(open(paths['svr'], 'rb'))
    res['scaler'] = pickle.load(open(paths['scaler'], 'rb'))
    #res['neural'] = torch.load(paths['neural'], map_location='cpu')
    return res

def load_paths():
    jsonFile = open('models_source.json')
    data = json.load(jsonFile)
    return data