# from data import *
from datetime import timedelta, time,date,datetime
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
    symbol: str           = None
    data:  pd.DataFrame   = None
    start: datetime.time  = None
    stop:  datetime.time  = None
    filepath = ".\\data\\stock_data\\day\\{}.csv"
    X_train,X_test,y_train,y_test = None,None,None,None

    def __init__(self,symbol:str,start:str="2018-01-01",stop:str="2019-01-01"):
        self.symbol = symbol
        self.start = datetime.strptime(start, '%Y-%m-%d')
        self.stop  = datetime.strptime(stop, '%Y-%m-%d')
        self.filepath = self.filepath.format(self.symbol)
        self.validate_stock()

    def validate_stock(self) -> bool:
        if type(self.symbol) != str:
            raise ValueError("self.symbol is not a str")
        if type(self.data) != pd.DataFrame and self.data != None:
            raise ValueError("self.data is not a pd.DataFrame")
        if self.start > self.stop:
            raise AssertionError("Your start is a newer date then your stopping date")
        return True

    def start_stop(self):
        self.start = self.data.index[0]
        self.stop = self.data.index[-1]

    def get_stock_data(self):
        """
        Gets data for a certain stock based on its symbol and return
        :param str symbol: The symbol of the stock, can only handle 1 name.
        :param bool output: Returns data if true\n"""
        # Checks that a start and stop date have been set
        # Checks that the stock is valid
        self.validate_stock()
        #check if data is already available
        if os.path.isfile(self.filepath):
            self.data = pd.read_csv(self.filepath,index_col='Date',parse_dates=True)
            return
        # Load & Select Data
        self.data = yf.download(self.symbol, start=self.start, end=self.stop,rounding=True)
        self.data = self.process_data(self.data)
        self.start_stop()
        # Save the data for later use
        self.data.to_csv(self.filepath,index=True)
        # Checks that the stock is valid
        self.validate_stock()

    def process_data(self,data:pd.DataFrame):
        # Fill empty data, select desired columns, and rename the "Adj Close" column to "Adj_Close".
        if data.isnull().sum().sum() != 0:
            raise Warning("You have " + data.isnull().sum().sum() + " null values in your data")
        data = data.fillna(0)
        data.rename(columns= {"Adj Close":"Adj_Close"},inplace=True)
        if 'Date' in data.columns.tolist():
            data.drop('Date',axis=1,inplace=True)
        return data

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


    def date_to_string(self,date:str):
        return date.strftime('%Y-%m-%d')

    def get_dates_to_update(self):
        print("get_dates_to_update()")
        new_start = None
        new_stop  = None
        now = datetime.now()
        last_open = now
        if now.weekday() > 4:
            last_open -= timedelta(now.weekday() % 4)
        print("The market was last open {}".format(last_open))
        # If the stop date is less than the last day that was open
        print(self.stop.date())
        print(last_open.date())
        if self.stop.date() < last_open.date():
            new_start = self.stop
            new_stop = last_open.date() + timedelta(days=1)
            print("new start\n",new_start)
            print("new stop\n",new_stop)
            return new_start,new_stop
        else:
            return None,None



    def update_data(self):
        print("update_data()")
        print(self.start,self.stop)
        new_start,new_stop = self.get_dates_to_update()
        print("update_data() new_start, should be None: ", new_start)
        if new_start == None:
            print("Everything is fully up to date")
            return
        print("new start and stop")
        print(str(new_start),str(new_stop))

        new_data = yf.download(self.symbol,start=new_start, end=new_stop,rounding=True)
        new_data = self.process_data(new_data)
        new_data.to_csv(self.filepath, mode="a",header=False,index=True)
        frames = [self.data,new_data]
        self.data = pd.concat(frames,axis=0)
        self.start_stop()
        print("after start_stop()")
        print(self.start)
        print(self.stop)




    # def train_test_split(self,X:pd.DataFrame=None,y:pd.DataFrame=None):

def main():
    aapl = Stock("AAPL","2010-01-01","2015-01-01")
    aapl.get_stock_data()
    aapl.update_data()
    # X,y = aapl.split_xy()


if __name__ == '__main__':
    main()








