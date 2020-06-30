import csv
from datetime import timedelta, time,date,datetime
import numpy as np
import os
import pandas as pd
import sys
import time
import yfinance as yf
sys.path.append('data/stock_data/day/')
from data.dictionary import *
from sklearn.model_selection import train_test_split

class Stock():
    """
    A stock data structure to hold stock data
    """
    symbol: str           = None
    data:  pd.DataFrame   = None
    start = None
    def __init__(self,symbol:str,start:str='2010-01-01'):
        self.switch_start(start)
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
        filepath = "data/stock_data/day/{}.csv"
        self.filepath = filepath.format(self.symbol)

    def get_data(self):
        return self.data

    def get_splits(self,window = 5,test_size = 0.2,target = 'pct',value = 0):
        if (target not in ['pct','diff','shift']):
            raise ValueError('{} is not an acceptable target, use ["pct","diff","shift"]'.format(target))
        elif not (type(window) == int):
            raise ValueError('Window must be an integer')
        elif not (type(test_size) == float):
            raise ValueError('test_size should be a float in range (0,1)')

        elif (target in ['pct','diff','shift']) & (type(window) == int) & (type(test_size) == float):
            columns = self.data.columns.tolist()
            columns.remove('Adj_Close')
            print(columns)
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

    def _to_dict(self):
        dictionary = dict()
        dictionary['symbol'] = self.symbol
        dictionary['start']  = self.start
        dictionary['stop']   = self.stop
        dictionary['filepath'] = self.filepath
        return dictionary
        # add code to send it to a csv

    def _validate_stock(self) -> bool:
        if type(self.symbol) != str:
            raise ValueError("self.symbol is not a str")
        if type(self.data) != pd.DataFrame and self.data != None:
            raise ValueError("self.data is not a pd.DataFrame")
        if self.start is not None and self.stop is not None:
            if self.start > self.stop:
                raise AssertionError("Your start is a newer date then your stopping date")
        return True

    def _set_start(self):
        self.start = datetime.date(self.data.index[0])

    def _set_stop(self):
        self.stop = datetime.date(self.data.index[-1])

    def _get_stock_data(self):
        #check if data is already available
        if os.path.isfile(self.filepath):
            self.data = pd.read_csv(self.filepath,index_col='Date',parse_dates=True)
            self.data = self.data.loc[self.start:]
            self._set_start()
            self._set_stop()
            return
        else:
            # Load & Select Data
            self.data = yf.download(self.symbol,start=self.start,rounding=True)
            # Save the data for later use
            self.data.to_csv(self.filepath,index=True)
            self._set_start()
            self._set_stop()

    def  _update_data(self) -> bool:
        """
        Updates stock data to the current date.
        :return bool: Whether the data got updated.
        """
        if date.today() == self.stop:
            return False
        new_start = self.stop + timedelta(days=1)
        new_data = yf.download(self.symbol,start=new_start,rounding=True)
        if new_data.empty or new_data.index[-1] <= self.data.index[-1]:
            return False
        else:
            new_data = new_data.loc[new_start:]
            # Save the data for later use
            new_data.to_csv(self.filepath, mode="a", index=True,header=False)
            # Save the data in self.data
            self.data = pd.concat([self.data,new_data]).drop_duplicates()
            self._set_stop()
            return True


def main():
    stock = Stock("AAPL")
    target = stock.get_data()['Adj_Close']
    target = pd.Series(target).pct_change(10).shift(-10).fillna(0).values
    print(target[-20:])

if __name__ == '__main__':
    main()
