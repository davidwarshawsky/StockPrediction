import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
from datetime import timedelta
from david.Stock import Stock
# Make sure to keep the date column
from keras.models import Model
from keras.layers import Input, Conv1D, Dense, Activation, Dropout, Lambda, Multiply, Add, Concatenate
from keras.optimizers import Adam

class Data():

    def __init__(self,stock:Stock):
        df = stock.get_data()
        self.data_start_date = df.columns[1]
        self.data_end_date = df.columns[-1]

        self.pred_steps = 100
        self.pred_length = timedelta(self.pred_steps)

        self.first_day = pd.to_datetime(self.data_start_date)
        self.last_day = pd.to_datetime(self.data_end_date)

        self.val_pred_start = self.last_day - self.pred_length + timedelta(1)
        self.val_pred_end = self.last_day

        self.train_pred_start = self.val_pred_start - self.pred_length
        self.train_pred_end = self.val_pred_start - self.timedelta(days=1)

        self.enc_length = self.train_pred_start - self.first_day

        self.train_enc_start = self.first_day
        self.train_enc_end = self.train_enc_start + self.enc_length - timedelta(1)

        self.val_enc_start = self.train_enc_start + self.pred_length
        self.val_enc_end = self.val_enc_start + self.enc_length - timedelta(1)

        print('Train encoding:', self.train_enc_start, '-', self.train_enc_end)
        print('Train prediction:', self.train_pred_start, '-', self.train_pred_end, '\n')

        print('Val encoding:', self.val_enc_start, '-', self.val_enc_end)
        print('Val prediction:', self.val_pred_start, '-', self.val_pred_end)

        print('\nEncoding interval:', self.enc_length.days)
        print('Prediction interval:', self.pred_length.days)

        self.date_to_index = pd.Series(index=pd.Index([pd.to_datetime(c) for c in df.index[:]]),
                                  data=[i for i in range(len(df.columns[1:]))])

        self.series_array = df.values

    def get_time_block_series(self,series_array, date_to_index, start_date, end_date):
        inds = date_to_index[start_date:end_date]
        return series_array[:, inds]

    def transform_series_encode(self,series_array):
        series_array = np.log(series_array)
        series_mean = series_array.mean(axis=1).reshape(-1, 1)
        series_array = series_array - series_mean
        series_array = series_array.reshape((series_array.shape[0], series_array.shape[1], 1))

        return series_array, series_mean

    def transform_series_decode(self,series_array, encode_series_mean):
        series_array = np.log(series_array)
        series_array = series_array - encode_series_mean
        series_array = series_array.reshape((series_array.shape[0], series_array.shape[1], 1))

        return series_array

    # extract training target at end
    def slice(self,x, seq_length):
        return x[:, -seq_length:, :]


if __name__ == '__main__':
    Data.testing(Stock("AAPL"))
