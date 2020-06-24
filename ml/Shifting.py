import numpy as np
import pandas as pd

import yfinance as yf
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from gplearn.genetic import SymbolicTransformer,SymbolicRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error,accuracy_score

def replace_bad(df):
    return df.replace(to_replace=[np.NaN, np.inf, -np.inf], value=0, inplace=True)


def retrieve_data(SYMBOL, start, stop, window_days):
    stock_data = yf.download(SYMBOL, start=start, end=stop, progress=False)

    replace_bad(stock_data)
    stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    stock_data.columns = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']

    stock_data['Balance'] = (stock_data['Close'] - stock_data['Open']) / (stock_data['High'] - stock_data['Low'])
    stock_data['CO'] = (stock_data['Close'] / stock_data['Open'])
    stock_data['HL'] = (stock_data['High'] / stock_data['Low'])
    stock_data['Open_Diff'] = (stock_data['High'] - stock_data['Low']) / stock_data['Open']

    Y = pd.DataFrame(stock_data['Adj_Close'].diff(periods=window_days).values, columns=[SYMBOL]).shift(-window_days)

    #     stock_data.drop(['Adj_Close','Close'],axis=1, inplace=True)
    stock_data.columns = [x + '_' + SYMBOL for x in list(stock_data.columns)]

    Y.reset_index(drop=True, inplace=True)
    stock_data.reset_index(drop=True, inplace=True)

    df_out_x = stock_data

    df_out_y = pd.DataFrame(Y)
    df_out_y_cat = np.where(df_out_y > 0, 1, 0)

    replace_bad(df_out_x)
    replace_bad(df_out_y)
    return df_out_x, df_out_y


def shifts(df, window):
    for col in df.columns.tolist():
        for i in range(1, window - 2):
            df[col + '_' + str(i)] = df[col].shift(-1 * i)
    replace_bad(df)
    return df
def categorical(real,pred,sample_weight = 0 ):
    pred = np.where(pred > 0 ,1,0)
    real = np.where(real > 0 ,1,0)
    return accuracy_score(real,pred)


table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
symbols = table[0]

for i, comp in enumerate(symbols['Symbol'].tolist()):
    if '.' in symbols.loc[i, 'Symbol']:
        symbols.loc[i, 'Symbol'] = symbols.loc[i, 'Symbol'].replace('.', '-')

invalid_stocks = ['CARR', 'CTVA', 'DOW', 'FOX', 'FOXA', 'HWM', 'OTIS', 'TT', 'VIAC']
Valid_Stock_Indexes = [i for i, x in enumerate(symbols['Symbol']) if symbols.loc[i, 'Symbol'] not in invalid_stocks]

symbols = symbols.loc[Valid_Stock_Indexes, :]
start = '2017-10-01'
stop = '2020-05-02'
shift_window_of_days = 10

for symbol in symbols['Symbol'].tolist():
    X, target = retrieve_data(symbol, start, stop, shift_window_of_days)
    X = shifts(X, shift_window_of_days)

    X_train, X_test, Y_train, Y_test = train_test_split(X, target, test_size=0.2, shuffle=False)

    lgr = SymbolicRegressor(stopping_criteria=5)
    #     lgr = LGBMRegressor(boosting_type='gbdt')

    lgr.fit(X_train, Y_train)
    predictions = lgr.predict(X_test)

    print(categorical(predictions, Y_test))
    print(mean_absolute_error(Y_test, predictions))
    print('-------------------------------------------------------------------------------')