import csv
from datetime import timedelta, time,date,datetime
import numpy as np
import os
import pandas as pd
import sys
import time
import yfinance as yf
sys.path.append('./data/')
sys.path.append('.\\data\\stock_data\\day')
from dictionary import *

invalid_stocks = []

class Stock():
    """
    A stock data structure to hold stock data
    """
    symbol: str           = None
    data:  pd.DataFrame   = None
    start = None
    stop  = None
    filepath = ".\\data\\stock_data\\day\\{}.csv"
    valid_name = True
    X_train,X_test,y_train,y_test = None,None,None,None

    def __init__(self,symbol:str):
        self.symbol = symbol
        self.filepath = self.filepath.format(self.symbol)
        #self.validate_stock()

    def get_data(self):
        return self.data

    def to_dict(self):
        dictionary = dict()
        dictionary['symbol'] = self.symbol
        dictionary['start']  = self.start
        dictionary['stop']   = self.stop
        dictionary['filepath'] = self.filepath
        return dictionary
        # add code to send it to a csv

    def validate_stock(self) -> bool:
        if type(self.symbol) != str:
            raise ValueError("self.symbol is not a str")
        if type(self.data) != pd.DataFrame and self.data != None:
            raise ValueError("self.data is not a pd.DataFrame")
        if self.start is not None and self.stop is not None:
            if self.start > self.stop:
                raise AssertionError("Your start is a newer date then your stopping date")
        return True

    # Sets the start and stop for after adding new data or reading it in from the csv
    def set_start_stop(self,start:datetime.time=None,stop:datetime.time=None):
        self.start= self.data.index[0]
        self.stop  = self.data.index[-1]

    def get_stock_data(self):
        #self.validate_stock()
        #check if data is already available
        if os.path.isfile(self.filepath):
            self.data = pd.read_csv(self.filepath,index_col='Date',parse_dates=True)
            self.set_start_stop()
            return
        else:
            # Load & Select Data
            self.data = yf.download(self.symbol,rounding=True)
            if self.data.shape[0] == 0:
                invalid_stocks.append(self.symbol)
                self.valid_name = False
                return
            self.data = self.process_data(self.data)
            # Save the data for later use
            self.data.to_csv(self.filepath,index=True)
            # Checks that the stock is valid
            # self.validate_stock()

    def process_data(self,data:pd.DataFrame):
        # Fill empty data, select desired columns, and rename the "Adj Close" column to "Adj_Close".
        if data.isnull().sum().sum() != 0:
            # raise Warning("You have " + data.isnull().sum().sum() + " null values in your data")
            data = data.fillna(0)
        data.rename(columns= {"Adj Close":"Adj_Close"},inplace=True)
        if 'Date' in data.columns.tolist():
            data.drop('Date',axis=1,inplace=True)
        return data

    def getXy(self,days=15):
        """
        Splits stock data into X and y.
        :param int days: The number of days to calculate percent change for y to predict the Adj_Close.
        :return pd.DataFrame X,y: X and y
        """
        data_copy = self.data.copy()
        y = data_copy['Adj_Close'].pct_change(periods=days).shift(-days).replace(to_replace=np.NaN, value=0)
        print(y)
        data_copy.drop(columns=['Adj_Close', 'Close'], axis=1, inplace=True)
        X = data_copy
        print(X.index[0],X.index[-1])
        print(y.index[0],y.index[-1])
        print(X.tail(20))
        print(y.tail(20))
        return X,y




    def update_data(self) -> bool:
        """
        Updates stock data to the current date.
        :return bool: data got updated.
        """
        if not self.valid_name:
            print("{} is not a valid stock name".format(self.symbol))
            return
        if date.today() == self.data.index[-1]:
            print("All data is up to date")
            return False
        self.set_start_stop()
        new_start = self.stop + timedelta(days=1)
        new_data = self.process_data(yf.download(self.symbol,start=new_start,rounding=True))
        if new_data.empty or new_data.index[-1] <= self.data.index[-1]:
            print("Up to date already\nnew data last index is {}\n old data last index is {}".format(new_data.index[-1],self.data.index[-1]))
            return False
        else:
            new_data = new_data.loc[new_start:]
            # Save the data for later use
            new_data.to_csv(self.filepath, mode="a", index=True,header=False)
            # Save the data in self.data
            self.data = pd.concat([self.data,new_data]).drop_duplicates()
            self.set_start_stop()
            return True


    # def train_test_split(self,X:pd.DataFrame=None,y:pd.DataFrame=None):

def main():
    aapl = Stock("AAPL")
    aapl.get_stock_data()
    aapl.update_data()
    X,y = aapl.getXy(days=14)
    # stocks:dict = csv_to_dict(open("./data/stocks.csv"))
    # for key in stocks.keys():
    #     print(key)
    #     stock = Stock(key.strip())
    #     stock.get_stock_data()
    #     stock.update_data()
    # with open("./data/invalid_stocks.csv",'w') as f:
    #     csv_writer = csv.writer(f)
    #     csv_writer.writerow(invalid_stocks)


if __name__ == '__main__':
    main()








