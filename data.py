import numpy as np
import os
import pandas as pd
import sys
sys.path.append('./data/')
import yfinance as yf
from dictionary import *


class Data():
    start = None
    stop  = None
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

    def get_stocks(self):
        """
        :param self:
        :return: A dictionary with stock tickers and industries from the S&P500.
        :rtype: dict()
        :raises Exception: If data is missing from the Wikipedia table
        """

        # If you already have the S&P 500 data, retrieve it locally
        if os.path.isfile("./stocks.csv"):
            return csv_to_dict(open("./data/stocks.csv"))
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
            # return the stocks dictionary
            return dictionary

    def get_prices(self,symbol,window_days):
        """
        Gets data for a certain stock based on its symbol and return
        :param str symbol: The symbol of the stock.
        :param int window_days: The number of days to calculate percent change for Y.
        :return: X,y
        int:
        """
        #Checks that a start and stop date have been set
        if (self.start == None or self.stop == None):
            raise ValueError("You forgot to set start and/or stop")
        # Load & Select Data
        stock_data = yf.download(symbol, start=self.start,end=self.stop)

        #Fill empty data, select desired columns, and rename the columns.
        if stock_data.isnull().sum().sum() != 0:
            raise Warning("You have " + stock_data.isnull().sum().sum() + " null values in your data")
        stock_data = stock_data.fillna(0)
        stock_data = stock_data[['Open', 'High', 'Low', 'Close','Adj Close', 'Volume']]
        stock_data.columns = ['Open', 'High', 'Low', 'Close','Adj_Close', 'Volume']


        Y = pd.DataFrame(stock_data['Adj_Close'].pct_change(periods = window_days).values,columns=[symbol]).shift(-window_days)

        stock_data.columns = [x+'_'+ symbol for x in list(stock_data.columns)]

        stock_data.drop(['Adj_Close_'+symbol,'Close_'+SYMBOL],axis=1, inplace=True)
        Y[SYMBOL].reset_index(drop =True, inplace =True)
        stock_data.reset_index(drop =True, inplace =True)

        X = stock_data.replace(to_replace=np.NaN,value = 0)
        y = pd.DataFrame(Y).replace(to_replace=np.NaN,value = 0)

        return X, y

    def get_data_and_features(self, window_days=15, symbols=None, industry=None):
        # If SYMBOL argument is provided and no industry is provided
        x_train = None
        y_train = None
        if (symbols != None):
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
    data.start_stop("2010-01-01","2010-01-01")

if __name__ == '__main__':
    main()
