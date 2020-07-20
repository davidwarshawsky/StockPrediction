from datetime import timedelta, date,datetime
import os
import pandas as pd
import sys
import yfinance as yf


def is_weekend(date:datetime.date):
    day_of_week = date.weekday()
    if day_of_week <= 4:
        return False
    else:
        return True

def get_slash():
    platform = sys.platform.lower()
    if "dar" not in platform:
        slash = "\\" # Windows
    else:
        slash = "/" # Linux or Mac
    return slash

def cd_wd():
    """
    Changes to StockPrediction as the working directory
    which is the sources root for any module in a subdirectory.
    :return:
    """
    sources_root = 'StockPrediction'
    slash = get_slash()
    paths = os.getcwd().split(slash) # List of directories
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

slash = get_slash()
data_dir = '.{0}data{0}stock_data{0}day{0}'.format(slash)

data_dir = data_dir.format(slash)
sys.path.append(data_dir)

# from sklearn.model_selection import train_test_split

class Stock():
    """
    A stock data structure to hold stock data
    """

    _symbol: str           = None
    _start: datetime.date  = None
    _path:str              = None
    up_to_date              = None

    def __init__(self,symbol:str=None,start:str='2010-01-01'):
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
        try:
            yf.Ticker(symbol).info
        except ImportError:
            message = "{} is not a valid yfinance symbol".format(symbol)
            raise ValueError(message)
        # If the symbol has available data, set it as the current symbol.
        self._symbol = symbol

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

    # def split(self,window = 5,test_size = 0.2,target = 'pct',value = 0):
    #     """"
    #     window: How many days ahead you want to predict the percent change for.
    #     value: What you would like  to fill nans with.
    #     """
    #     if target not in ['pct','diff','shift']:
    #         raise ValueError('{} is not an acceptable target, use ["pct","diff","shift"]'.format(target))
    #     elif not (type(window) == int):
    #         raise ValueError('Window must be an integer')
    #     elif not (type(test_size) == float):
    #         raise ValueError('test_size should be a float in range (0,1)')
    #
    #     elif (target in ['pct','diff','shift']) & (type(window) == int) & (type(test_size) == float):
    #         columns = self.data.columns.tolist()
    #         columns.remove('Adj_Close')
    #         if target == 'pct':
    #             y = self.data['Adj_Close'].pct_change(window).shift(-window,fill_value = value)
    #         elif target == 'diff':
    #             y = self.data['Adj_Close'].diff(window).shift(-window,fill_value = value)
    #         elif target == 'shift':
    #             y = self.data['Adj_Close'].shift(-window,fill_value = value)
    #
    #         X = self.data[columns]
    #         X = X.iloc[:int(self.data.shape[0]-window),:]
    #         y = y[:int(self.data.shape[0]-window)]
    #
    #         X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = test_size)
    #         return X_train, X_test, y_train, y_test

if __name__ == '_main_':
    pass
