import numpy as np
import os
import pandas as pd
import sys
sys.path.append('./data/')
sys.path.append('./data/stock_data/day')
import yfinance as yf
from dictionary import *


class Data():
    start = None
    stop  = None
    stocks = None
    data = dict()
    """
    Access stock data
    """
    def __init__(self):
        """
        Initializes Data class.
        """

    def start_stop(self,start:str=None,stop:str=None):
        """
        :param self:
        :param str start: Date to start getting data. "YYYY-MM-DD"
        :param str stop: Date to stop getting data.  "YYYY-MM-DD"
        """
        self.start = start
        self.stop = stop

    def get_stocks(self, output=None):
        """
        :param self:
        :return: A dictionary with stock tickers and industries from the S&P500.
        :raises Exception: If data is missing from the Wikipedia table
        :param bool output: Returns data if true\n"""

        # If you already have the S&P 500 data, retrieve it locally
        if os.path.isfile("./data/stocks.csv"):
            self.stocks = csv_to_dict(open("./data/stocks.csv"))
        # Retrieve S&P500 table from Wikipedia
        else:
            table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
            table.columns = [x.strip() for x in table.columns]
            # Select only the two columns needed
            df = table.loc[:,['Symbol','GICS Sub Industry']]
            # Raises an exception if the Wikipedia call is missing values
            if df.isnull().any().any():
                raise Exception("There are NaN stock symbols or industries")

            # Create a fast lookup for stock and industries
            dictionary = dict(zip(table.Symbol.tolist(),table["GICS Sub Industry"].tolist()))

            # Write the dictionary to a csv file for later
            dict_to_csv(open("./data/stocks.csv", "w", newline=""),dictionary)
            # save the stocks dictionary
            self.stocks = dictionary
        if output  == True:
            return self.stocks
     def stock_data_loaded(self,s  ):

    def valid_symbol(self):
        if (self.start == None or self.stop == None):
            raise ValueError("You forgot to set start and/or stop")
        return True

    def get_stock_data(self,symbol=None,output=None):
        """
        Gets data for a certain stock based on its symbol and return
        :param str symbol: The symbol of the stock, can only handle 1 name.
        :param bool output: Returns data if true\n"""
        #Checks that a start and stop date have been set
        # Checks that the stock is valid
        self.valid_symbol(symbol)
        # Load & Select Data
        stock_data = yf.download(symbol, start=self.start,end=self.stop)

        #Fill empty data, select desired columns, and rename the columns.
        if stock_data.isnull().sum().sum() != 0:
            raise Warning("You have " + stock_data.isnull().sum().sum() + " null values in your data")
        stock_data = stock_data.fillna(0)
        stock_data = stock_data[['Open', 'High', 'Low', 'Close','Adj Close', 'Volume']]
        stock_data.columns = ['Open', 'High', 'Low', 'Close','Adj_Close', 'Volume']
        self.data[symbol] = stock_data
        if output  == True:
            return stock_data

    def split_xy(self,symbol=None,window_days=None,output=None):
        """
        Splits stock data.
        :param int window_days: The number of days to calculate percent change for Y.
        :return: X,y
        :param bool output: Returns data if true\n"""
        self.valid_symbol(symbol)
        if window_days is not None:
            y = pd.DataFrame(self.data[symbol]['Adj_Close'].pct_change(periods = window_days).values,columns=[symbol]).shift(-window_days)
        else:
            y = pd.DataFrame(self.data[symbol]['Adj_Close'])

        # The line below does not seem necessary
        #stock_data.columns = [x+'_'+ symbol for x in list(stock_data.columns)]

        self.data[symbol].drop(['Adj_Close','Close'],axis=1, inplace=True)
        self.data[symbol].reset_index(drop=True, inplace=True)
        y[symbol].reset_index(drop =True, inplace =True)


        X = self.data[symbol].replace(to_replace=np.NaN,value = 0)
        y = pd.DataFrame(y).replace(to_replace=np.NaN,value = 0)
        if output == True:
            return X,y

    def train_test_split(self, window_days: int = None, output=None):
        X_train = None
        X_test = None
        y_train = None
        y_test  = None

        if output == True:
            return X_train,X_test,y_train,y_test
        
    def get_data_and_features(self, window_days=15, symbols=None, industry=None):
        # If SYMBOL argument is provided and no industry is provided
        x_train = None
        y_train = None
        if symbols != None:
            # It is a single stock.
            if type(symbols) == str:
                try:
                    x_train, y_train = self.retrieve_data(symbols,self.start,self.stop,window_days)
                except KeyError:
                    x_train, y_train = self.retrieve_data(symbols,self.start,self.stop,window_days)
            # It is an array of stocks.
            else:
                for symbol in symbols:
                    try:
                        stock_data,Y = self.retrieve_data(symbol,self.start,self.stop,window_days)
                    except KeyError:
                        stock_data,Y = self.retrieve_data(symbol,self.start,self.stop,window_days)
                    x_train = pd.concat((x_train,stock_data),axis=1)
                    y_train = pd.concat((y_train,Y),axis=1)

        # If an industry is provided
        if (type(industry) == str):
            symbol_dataframe = self.get_stocks()
            symbol_list = list(symbol_dataframe.loc[symbol_dataframe['Industry'] == industry,'Tickers'])

            # For each symbol in the array of symbols
            for symbol in symbol_list:
                try:
                    stock_data,Y = self.retrieve_data(symbol,self.start,self.stop,window_days)
                except KeyError:
                    stock_data,Y = self.retrieve_data(symbols,self.start,self.stop,window_days)

                x_train = pd.concat((x_train,stock_data),axis=1)
                y_train = pd.concat((y_train,Y),axis=1)
        # works
        return x_train.replace(to_replace=np.nan,value = 0), y_train.replace(to_replace=np.nan,value = 0)


def main():
    data = Data()
    data.start_stop("2010-01-01","2015-01-01")
    print(data.get_stocks(output=True))

if __name__ == '__main__':
    main()
