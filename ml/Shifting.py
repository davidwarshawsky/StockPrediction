import pickle
import numpy as np
import pandas as pd
import sys
sys.path.append('ml/models/')
sys.path.append('data/stock_data/predictions/')
import yfinance as yf
import matplotlib.pyplot as plt
from data import Stock
from sklearn.model_selection import train_test_split
from gplearn.genetic import SymbolicTransformer,SymbolicRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error,accuracy_score
from ml.BaseModel import BaseModel

class SymbolicRegressor(BaseModel):

    def __init__(self):
        super(SymbolicRegressor(stopping_criteria=5))

    def save(self):
        with open('ml/models/symbolicregressor5.pkl', 'wb') as f:
            pickle.dump(self.symR, f)


    def load_model(self):
        with open('ml/models/symbolicregressor5.pkl', 'rb') as f:
            self.symR = pickle.load(f)
            # Error allowed to each sample.


# from data.TS import shifts
from emailer import send_email

def main():
    stuff =
    # send_email("davidawarshawsky@gmail.com", "Come on hear me out", message)

if __name__ == '__main__':
    main()