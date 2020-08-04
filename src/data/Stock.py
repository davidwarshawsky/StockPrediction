from datetime import timedelta, date,datetime
import os
import numpy as np
import pandas as pd
import sys
import yfinance as yf
from main import ModelPredictorSP500


def is_weekend(date:datetime.date):
    day_of_week = date.weekday()
    if day_of_week <= 4:
        return False
    else:
        return True



def cd_wd():
    """
    Changes to StockPrediction as the working directory
    which is the sources root for any module in a subdirectory.
    :return:
    """
    sources_root = 'StockPrediction'
    paths = os.getcwd().split(os.path.sep) # List of directories
    try:
        target_index = paths.index(sources_root)
        for _ in range(len(paths) - target_index - 1):
            os.chdir('..')
    except ValueError:
        message = "The root <{}> is not valid".format(sources_root)
        raise ValueError(message)

cd_wd()
from src.features.TS import validate
print(os.getcwd())

data_dir = '.{0}data{0}stock_data{0}day{0}'.format(os.path.sep)

data_dir = data_dir.format(os.path.sep)
sys.path.append(data_dir)

# from sklearn.model_selection import train_test_split

class Stock():
    """
    A stock data structure to hold stock data
    """

    _symbol: str           = None
    _start: datetime.date  = None
    _path:str              = None
    up_to_date             = None
    valid_symbols          = None

    def __init__(self,symbol:str=None,start:str='2010-01-01'):
        self.valid_symbols = ModelPredictorSP500.read_SP500_symbols()
        # Set the start regardless of if there is a symbol provided.
        self.switch_start(start)
        # If the symbol is provided, switch to it.
        if symbol is not None:
            self.switch_stock(symbol)

    @property
    def data(self):
        return self._all_data.loc[self._start:]

    @property
    def stop(self):
        return datetime.date(self.data.index[-1])

    @property
    def up_to_date(self):
        if date.today() == self.stop:
            return True
        else:
            return False

    def get_start(self):
        return datetime.date(self._all_data.index[0])
    

    def switch_stock(self,symbol):
        # Do nothing if you try to switch to the same symbol.
        if self._symbol == symbol:
            # For unit testing purposes, return False.
            return False
        self.__set_symbol(symbol)
        self.__set_path()
        self.__retrieve_data()
        self.__update_data()

    def switch_start(self,start:str='2010-01-01'):
        # Check that the date fits the proper format.
        validate(start)
        # Extract the date.
        new_start = datetime.strptime(start, '%Y-%m-%d')
        # If the date provided is the same as the current date then do nothing.
        if self._start == new_start:
            # For unit testing purposes, return False.
            return False
        # If the date provided is different than the last, change it to the current date.
        # Closer to present is larger
        else:
            self._start = new_start

    def __set_symbol(self,symbol):
        # Check if the symbol has data available.
        if symbol in self.valid_symbols:
            self._symbol = symbol
        else:
            message = "{} is not a valid yfinance symbol".format(symbol)
            raise ValueError(message)


    def __set_path(self):
        path:str = data_dir + "{}.csv"
        self._path = path.format(self._symbol)

    def __save_data(self,df,append=False):
        if not append:
            df.to_csv(self._path,index=True)
        else:
            df.to_csv(self._path, mode="a", index=True, header=False)


    def __process_data(self, df: pd.DataFrame):
        return df.rename(columns={'Adj Close': 'Adj_Close'})

    def __retrieve_data(self):
        #check if data is already available
        if os.path.isfile(self._path):
            # Read in all data and select a subset based on the start in case last time
            # the Stock was called an earlier start date was used.
            self._all_data = pd.read_csv(self._path,index_col='Date',parse_dates=True)
            return "r"
        else:
            # Load & Select ALL Data, you don't get a choice.
            # You get to choose a subsection of ALL THE DATA.
            data = yf.download(self._symbol,rounding=True)
            self._all_data = self.__process_data(data)
            # Save the data for later.
            self.__save_data(self._all_data,append=False)
            # Return
            return "w"


    def  __update_data(self) -> bool:
        """
        Updates stock data to the current date.
        :return bool: Whether the data got updated.
        """
        # If the date of the last index of data is today return False
        if self.up_to_date:
            return False
        # Add one day to the current stop to get a new start.
        new_start = self.stop + timedelta(days=1)
        # Get new data based on the new start.
        new_data = yf.download(self._symbol,start=new_start,rounding=True)
        new_data = self.__process_data(new_data)
        """
        If there is no new data or the last index of the new data
        is further back than the current data then return False.
        """
        if new_data.empty or new_data.index[-1] <= self._all_data.index[-1]:
            return False
        # If you have new valid data
        else:
            self._all_data = pd.concat([self._all_data,new_data])
            self.__save_data(new_data,append=True)
            return True

    def split_features(self):
        columns = self._all_data.columns.tolist()
        print(columns)
        columns.remove('Adj_Close')
        X = X = self._all_data[columns]
        y = self._all_data['Adj_Close']
        return X, y

    def split(self, transpose=True, window=10, test_size=0.2, target='pct', value=0):
        """"
        test_size: Fraction of data that will be used as test/validation sets
        target: How to generate target data
        window: How many days ahead you want to predict the percent change for.
        value: What you would like  to fill nans with.
        """
        if target not in ['pct', 'diff', 'shift']:
            raise ValueError('{} is not an acceptable target, use ["pct","diff","shift"]'.format(target))
        elif not (type(window) == int):
            raise ValueError('Window must be an integer')
        elif not (type(test_size) == float):
            raise ValueError('test_size should be a float in range (0,1)')

        elif (target in ['pct', 'diff', 'shift']) & (type(window) == int) & (type(test_size) == float):
            X, y = self.split_features()
            if target == 'pct':
                y = y.pct_change(window).shift(-window, fill_value=value)
            elif target == 'diff':
                y = y.diff(window).shift(-window, fill_value=value)
            elif target == 'shift':
                y = y.shift(-window, fill_value=value)

            train_size = int(X.shape[0] * (1 - test_size))
            future_features = X.iloc[int(self._all_data.shape[0] - window):, :]
            X = X.iloc[:int(self._all_data.shape[0] - window), :]
            y = pd.DataFrame(y[:int(self._all_data.shape[0] - window)])

            X_train, X_test, y_train, y_test = X.iloc[:train_size, :], X.iloc[train_size:, :], y[:train_size], y[
                                                                                                               train_size:]

            def transpose_df(df):
                return np.array(df).reshape((df.shape[0], 1, -1))

            if transpose:
                transposed_dfs = [transpose_df(df) for df in [X_train, X_test, y_train, y_test, future_features]]
                return transposed_dfs[0], transposed_dfs[1], transposed_dfs[2], transposed_dfs[3], transposed_dfs[4]
            else:
                return X_train, X_test, y_train, y_test, future_features

if __name__ == '_main_':
    pass