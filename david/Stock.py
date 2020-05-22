from data import *
import numpy as np
import os
import pandas as pd
import sys
import yfinance as yf
sys.path.append('.\\data\\stock_data\\day')

class Stock():
    """
    A stock data structure to hold stock data
    """
    symbol = None
    data   = None
    start  = None
    stop   = None
    X_train,X_test,y_train,y_test = None,None,None,None

    def __init__(self,symbol:str,start:str="2018-01-01",stop:str="2019-01-01"):
        self.symbol = symbol
        self.start = start
        self.stop = stop

    def validate_stock(self) -> bool:
        if type(self.symbol) != str:
            raise ValueError("self.symbol is not a str")
        if type(self.data) != pd.DataFrame and self.data != None:
            raise ValueError("self.data is not a pd.DataFrame")
        return True

    def get_stock_data(self):
        """
        Gets data for a certain stock based on its symbol and return
        :param str symbol: The symbol of the stock, can only handle 1 name.
        :param bool output: Returns data if true\n"""
        # Checks that a start and stop date have been set
        # Checks that the stock is valid
        self.validate_stock()
        #check if data is already available
        filepath = ".\\data\\stock_data\\day\\{}.csv".format(self.symbol)
        if os.path.isfile(filepath):
            self.data = pd.read_csv(filepath)
            print("Data already available for {}".format(self.symbol))
            return
        # Load & Select Data
        self.data = yf.download(self.symbol, start=self.start, end=self.stop)

        # Fill empty data, select desired columns, and rename the "Adj Close" column to "Adj_Close".
        if self.data.isnull().sum().sum() != 0:
            raise Warning("You have " + self.data.isnull().sum().sum() + " null values in your data")
        self.data = self.data.fillna(0)
        self.data.rename(columns= {"Adj Close":"Adj_Close"},inplace=True)
        # Save the data for later use
        print("writing the data for {}".format(self.symbol))
        self.data.to_csv(filepath)
        # Checks that the stock is valid
        self.validate_stock()

    def split_xy(self,predict_days=15):
        """
        Splits stock data into X and y.
        :param int predict_days: The number of days to calculate percent change for y to predict the Adj_Close.
        :return pd.DataFrame X,y: X and y
        """
        # Checks that the stock is valid
        self.validate_stock()

        y = pd.DataFrame(self.data['Adj_Close'].pct_change(periods = predict_days).values,columns=[self.symbol]).shift(-predict_days)

        # Why would you drop today's close if you are predciting the adjusted close in the future?
        self.data.drop(['Adj_Close','Close'],axis=1, inplace=True)
        self.data.reset_index(drop=True, inplace=True)
        y.reset_index(drop =True, inplace =True)


        X = self.data.replace(to_replace=np.NaN,value = 0)
        y = pd.DataFrame(y).replace(to_replace=np.NaN,value = 0)
        # Checks that the stock is valid
        self.validate_stock()
        print("X shape: {} \nX columns:{}\ny shape: {}\ny columns:{}".format(X.shape,X.columns,y.shape,y.columns))
        return X,y

    # def train_test_split(self,X:pd.DataFrame=None,y:pd.DataFrame=None):

def main():
    aapl = Stock("AAPL","2010-01-01","2015-01-01")
    aapl.get_stock_data()
    X,y = aapl.split_xy()

if __name__ == '__main__':
    main()








