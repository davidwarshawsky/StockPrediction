import csv
from datetime import timedelta, time,date,datetime
import numpy as np
import os
import pandas as pd
import sys
import time
import yfinance as yf
sys.path.append('../data/stock_data/day/')
from dictionary import *


class Stock():
    """
    A stock data structure to hold stock data
    """
    symbol: str           = None
    data:  pd.DataFrame   = None
    start = None
    filepath = "../data/stock_data/day/{}.csv"

    def __init__(self,symbol:str,start:str='2010-01-01'):
        self.symbol = symbol
        self.filepath = self.filepath.format(self.symbol)
        self.start = datetime.strptime(start,'%Y-%m-%d')

    def get_data(self):
        return self.data

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

    def get_stock_data(self):
        #check if data is already available
        if os.path.isfile(self.filepath):
            self.data = pd.read_csv(self.filepath,index_col='Date',parse_dates=True)
            self.set_start()
            self.set_stop()
            return
        else:
            # Load & Select Data
            self.data = yf.download(self.symbol,start=self.start,rounding=True)
            # Save the data for later use
            self.data.to_csv(self.filepath,index=True)
            self.set_start()
            self.set_stop()

    def update_data(self) -> bool:
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
            self.set_stop()
            return True
