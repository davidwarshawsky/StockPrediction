import csv
from datetime import timedelta, time,date,datetime
import numpy as np
import os
import pandas as pd
import sys
import time
import yfinance as yf
sys.path.append('./appdata/stock_data/day/')
from appdata.dictionary import *
from sklearn.model_selection import train_test_split

class Stock():
    """
    A stock data structure to hold stock data
    """
    symbol: str           = None
    data:  pd.DataFrame   = None
    start = None
    def __init__(self,symbol:str=None,start:str='2010-01-01'):
        self.switch_start(start)
        if symbol is not None:
            self.switch_stock(symbol)

    def switch_stock(self,symbol):
        self._set_symbol(symbol)
        self._set_filepath()
        self._get_stock_data()
        self._update_data()

    def switch_start(self,start:str='2010-01-01'):
        self.start = datetime.strptime(start, '%Y-%m-%d')

    def _set_symbol(self,symbol):
        self.symbol = symbol

    def _set_filepath(self):
        filepath = "appdata\\stock_data\\day\\{}.csv"
        self.filepath = filepath.format(self.symbol)

    def get_data(self):
        return self.data

    def get_splits(self,window = 5,test_size = 0.2,target = 'pct',value = 0):
        """"
        window: How many days ahead you want to predict the percent change for.
        value: What you would like  to fill nans with.
        """
        if target not in ['pct','diff','shift']:
            raise ValueError('{} is not an acceptable target, use ["pct","diff","shift"]'.format(target))
        elif not (type(window) == int):
            raise ValueError('Window must be an integer')
        elif not (type(test_size) == float):
            raise ValueError('test_size should be a float in range (0,1)')

        elif (target in ['pct','diff','shift']) & (type(window) == int) & (type(test_size) == float):
            columns = self.data.columns.tolist()
            columns.remove('Adj_Close')
            if target == 'pct':
                y = self.data['Adj_Close'].pct_change(window).shift(-window,fill_value = value)
            elif target == 'diff':
                y = self.data['Adj_Close'].diff(window).shift(-window,fill_value = value)
            elif target == 'shift':
                y = self.data['Adj_Close'].shift(-window,fill_value = value)

            X = self.data[columns]
            X = X.iloc[:int(self.data.shape[0]-window),:]
            y = y[:int(self.data.shape[0]-window)]

            X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = test_size)
            return X_train, X_test, y_train, y_test


    def _set_start(self):
        self.start = datetime.date(self.data.index[0])

    def _set_stop(self):
        self.stop = datetime.date(self.data.index[-1])

    def _get_stock_data(self):
        #check if data is already available
        if os.path.isfile(self.filepath):
            print(self.filepath)
            self.data = pd.read_csv(self.filepath,index_col='Date',parse_dates=True)
            self.data = self.data.loc[self.start:]
            self._set_stop()
            print("Got data from csv")
        else:
            # Load & Select Data
            self.data = yf.download(self.symbol,start=self.start,rounding=True)
            self.data = self.data.rename(columns={'Adj Close':'Adj_Close'})
            # Save the data for later use and set the stop index
            self.data.to_csv(self.filepath,index=True)
            self._set_stop()

    def  _update_data(self) -> bool:
        """
        Updates stock data to the current date.
        :return bool: Whether the data got updated.
        """
        # If the date of the last index of data is today return False
        if date.today() == self.stop:
            print("Todays date equals stopping date so didn't update data")
            return False
        print("UPDATING")
        # Add one day to the current stop to get a new start.
        new_start = self.stop + timedelta(days=1)
        # Get new data based on the new start.
        new_data = yf.download(self.symbol,start=new_start,rounding=True)
        # If there is no new data or the last index of the new data
        # is further back than the current data then return False.
        if new_data.empty or new_data.index[-1] <= self.data.index[-1]:
            print("There is no new data to add")
            return False
        # If you have new valid data
        else:
            new_data = new_data.rename(columns={'Adj Close': 'Adj_Close'})
            # Select the new_data from the new_start
            # new_data = new_data.loc[new_start:]
            # Save the data for later use
            new_data.to_csv(self.filepath, mode="a", index=True,header=False)
            # Add the new data to self.data and drop duplicates just in case.
            self.data = pd.concat([self.data,new_data]).drop_duplicates()
            print(self.data.shape)
            # Set the new stop and return True.
            self._set_stop()
            return True

if __name__ == '__main__':
    stockHandler = Stock()
    stockHandler.switch_stock("GOOG")