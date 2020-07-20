# File that defines functions for time series.
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from datetime import datetime

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    """
    Frame a time series as a supervised learning dataset.
    Arguments:
        data: Sequence of observations as a list or NumPy array.
        n_in: Number of lag observations as input (X).
        n_out: Number of observations as output (y).
        dropnan: Boolean whether or not to drop rows with NaN values.
    Returns:
        Pandas DataFrame of series framed for supervised learning.
    """
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


def get_last_days(index,days):
    return index[-days:]

def time_series_split(df:pd.DataFrame,days):
    # Drop volume because it overpowers everything else in the model
    df.drop(columns=['Volume'],inplace=True)
    # df.reset_index(drop=True,inplace=True)
    # Scale data without min max.
    df = df.div(100)
    # Get the number of rows
    data_size = df.shape[0]
    copy = series_to_supervised(df.values, days, 1 )
    copy.drop(columns=['var1(t)', 'var2(t)', 'var3(t)', 'var4(t)','var5(t)'],inplace=True,axis=1)
    # ---
    values = copy.values
    values[:, -1] = pd.Series(values[:, -1].flatten()).pct_change(days).shift(-days).fillna(0).values
    train_size = int(values.shape[0] * 0.8)
    train = values[:train_size, :]
    test = values[train_size:, :]
    future_features = test[-days:, :-1]
    test = test[:-days,:]
    # split into input and outputs
    X_train, y_train = train[:, :-1], train[:, -1]
    X_test, y_test = test[:, :-1], test[:, -1]
    # reshape input to be 3D [samples, timesteps, features]
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))
    y_train = y_train.reshape(y_train.shape[0], 1, 1)
    y_test = y_test.reshape(y_test.shape[0], 1, 1)
    future_features = future_features.reshape(future_features.shape[0],1,future_features.shape[1])
    return X_train,y_train,X_test,y_test,future_features

def shifts(df, window):
    for col in df.columns.tolist():
        for i in range(1, window - 1):
            df[col + '_' + str(i)] = df[col].shift(-1 * i)
    replace_bad(df)
    return df

def holdout_confidence(real,pred,sample_weight = 0 ):
    #provides accuracy dependant on the trend changes in a holdout set:
      # where class 1 is positive trend
     #  and class 0 is negative trend
    pred = np.where(pred > 0 ,1,0)
    real = np.where(real > 0 ,1,0)
    return accuracy_score(real,pred)
