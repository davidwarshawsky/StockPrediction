import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from gplearn.genetic import SymbolicRegressor
# from lightgbm import LGBMRegressor
from sklearn.linear_model import (HuberRegressor,BayesianRidge,OrthogonalMatchingPursuit)
from sklearn.ensemble import (VotingRegressor,StackingRegressor)

from sklearn.metrics import (mean_absolute_error, accuracy_score)
from src.features.Feature_Generator import FeatureGenerator
from src.data.Stock import Stock

def get(ticker = 'AAPL'):
    time_frame = 20
    window = 40
    Handler = Stock(ticker)
    X = Handler._all_data
    y = Handler.create_target(X,window = window)
    FG = FeatureGenerator()
    X = FG.shifts(X,window = window,time_frame = time_frame)
    X_train, X_test, y_train, y_test, future_features = Handler.split(X,y,transpose=False, window = time_frame)
    return X_train, X_test, y_train, y_test, future_features

def get_linear_model(model_type = 'stacker'):
    HR = HuberRegressor(max_iter=8000)
    BR = BayesianRidge()
    OMP = OrthogonalMatchingPursuit()
    if model_type == 'stacker':
        model = StackingRegressor(estimators=[('BR', BR), ('OMP', OMP), ('HR', HR)])
    if model_type == 'voter':
        model = VotingRegressor(estimators=[('BR', BR), ('OMP', OMP), ('HR', HR)])
    if model_type == 'genetic':
        model = SymbolicRegressor()
    return model

def eval(ticker = 'F'):
    X_train, X_test, y_train, y_test, future_features = get(ticker)
    for model_t in ['genetic','stacker','voter']:
        model = get_linear_model(model_t)
        model.fit(X_train,y_train)
        valid_set_predictions = model.predict(X_test)
        FG = FeatureGenerator()
        print(FG.categorical(valid_set_predictions, y_test))
        print(FG.mae(valid_set_predictions, y_test))
        print(model.predict(future_features))

def main():
    # X_train, X_test, y_train, y_test, future_features = get()
    # print(future_features.index)
    eval()

if __name__ == '__main__':
    main()
