import numpy as np
import pandas as pd

import yfinance as yf
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from gplearn.genetic import SymbolicTransformer,SymbolicRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error,accuracy_score

from data.TS import shifts
from emailer import send_email

def main():
    ticker = Stock("MSFT")
    X_train, X_test, y_train, y_test = ticker.get_splits()
    symb = SymbolicRegressor(stopping_criteria=5)
    symb.fit(X_train, Y_train)
    pred = str(symb.predict(X_test).flatten()[-1])

    message = "Microsoft percent change for tommorow" + ": " + pred
    send_email("davidawarshawsky@gmail.com", "Come on hear me out", message)

if __name__ == '__main__':
    main()