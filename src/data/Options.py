import yfinance as yf
import pandas as pd
import os
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
import sys
import numpy as np
from datetime import datetime
sys.path.append('data{0}stock_data{0}options{0}'.format(os.path.sep))
from src.features.TS import validate
from src.features.TSDS import TSDS

# https://github.com/mcdallas/wallstreet

class Options():
    """
    A stock data structure to hold stock data
    """
    _puts: pd.DataFrame
    _calls: pd.DataFrame
    _symbol: str = None
    _ticker: yf.Ticker
    _puts_path  = None
    _calls_path = None
    _dates      = None
    _start      = None

    def __init__(self,symbol:str=None,start:str='2010-01-01'):
        """

        :rtype: object
        """
        # Set the start regardless of if there is a symbol provided.
        self.switch_start(start)
        # If the symbol is provided, switch to it.
        if symbol is not None:
            self.switch_stock(symbol)

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
        if self._start is not None and self._start == new_start:
            # For unit testing purposes, return False.
            return False
        # If the date provided is different than the last, change it to the current date.
        # Closer to present is larger
        else:
            self._start = new_start
            return True

    def __set_symbol(self,symbol):
        # Check if the symbol has data available.
        try:
            yf.Ticker(symbol).info
        except ImportError:
            message = "{} is not a valid yfinance symbol".format(symbol)
            raise ValueError(message)
        # If the symbol has available data, set it as the current symbol.
        self._symbol = symbol
        self._ticker = yf.Ticker(self._symbol)

    def __set_path(self):
        # Format the filepath
        calls_path = "data{0}stock_data{0}options{0}c{1}.csv"
        puts_path = "data{0}stock_data{0}options{0}p{1}.csv"
        self._calls_path = calls_path.format(os.path.sep,self._symbol)
        self._puts_path = puts_path.format(os.path.sep,self._symbol)

    def __retrieve_data(self):
        """
        Retrieves puts and calls dataframes from csv.
        :return:
        """
        # check if data is already available
        if os.path.isfile(self._calls_path) and os.path.isfile(self._puts_path):
            self._calls = pd.read_csv(self._calls_path, index_col=[0, 1])
            self._puts = pd.read_csv(self._puts_path, index_col=[0, 1])
            self._dates = list(self._calls.index.get_level_values(0).unique())
            self._puts.index = self._puts.index.set_levels([pd.to_datetime(self._puts.index.levels[0]),
                                            self._puts.index.levels[1]])
            self._calls.index = self._calls.index.set_levels([pd.to_datetime(self._calls.index.levels[0]),
                                                            self._calls.index.levels[1]])

            return "r"
        else:
            print("GETTING FRESH")
            # Getting chains
            dates = self.__get_options_dates(self._ticker)
            self._dates = dates
            chains = self.__get_options_chains(self._ticker, dates)
            # Setting
            self._puts = self.__process_data(self.__get_puts(chains), dates)
            self._calls = self.__process_data(self.__get_calls(chains), dates)
            # Save data for later
            self.__save_data(self._calls,self._calls_path,append=False)
            self.__save_data(self._puts,self._puts_path,append=False)
            return "w"


    def __get_options_dates(self,ticker):
        """
        Gets the dates available for options for a stock.
        """
        return list(ticker.options)

    def __get_options_chains(self,ticker,date):
        """
        Gets option chains for a stock.
        :param date: The date or dates for the options chains.
        :return: A list of option chains
        """
        chains = []
        if type(date) == list:
            for d in date:
                chains.append(ticker.option_chain(d))

        if type(date) == str:
            chains.append(ticker.option_chain(date))

        return chains

    def __get_calls(self,chains):
        """
        Gets calls from option chains..
        """
        calls = []
        for chain in chains:
            calls.append(chain.calls)
        return calls

    def __get_puts(self,chains):
        """
        Gets puts from option chains.
        """
        puts = []
        for chain in chains:
            puts.append(chain.puts)
        return puts

    def __process_data(self,df, dates):
        df = pd.concat(df, keys=dict(zip(dates, df)))
        df['inTheMoney'] = df['inTheMoney'].replace({False: 0, True: 1})
        df['inTheMoney'] = df['inTheMoney'].astype(np.bool)
        df['impliedVolatility'] = df['impliedVolatility'].astype(np.int32)
        df = df.drop(columns=['lastTradeDate','contractSymbol', 'contractSize', 'currency'])
        df = df.round(2)
        # https://stackoverflow.com/questions/18835077/selecting-from-multi-index-pandas/49045951
        # https://stackoverflow.com/questions/45243291/parse-pandas-multiindex-to-datetime
        # https://stackoverflow.com/questions/33801584/pandas-multi-index-slicing-level-type-mismatch
        df.index = df.index.set_levels([pd.to_datetime(df.index.levels[0]),
                                        df.index.levels[1]])
        return df

    def __save_data(self, df, path,append=False):
        if not append:
            df.to_csv(path, index=True)
        else:
            df.to_csv(path, mode="a", index=True, header=False)

    def __update_data(self):
        # Get all current available dates for options
        options_dates = self.__get_options_dates(self._ticker)
        # If there are new dates available for options, select them.
        new_dates = [x for x in options_dates if x not in self._dates]
        print("__update_data() new_dates: {}".format(new_dates))
        if new_dates:
            # Get dates to update
            # Add new dates to dates
            self._dates = self._dates.append(new_dates)
            print("__update_data() self._dates: {}".format(self._dates))
            # Get new options and process them
            # Get new options and process them
            new_chains = self.__get_options_chains(self._ticker, new_dates)

            new_calls = self.__get_calls(new_chains)
            new_processed_calls = self.__process_data(new_calls, new_dates)
            new_puts = self.__get_puts(new_chains)
            new_processed_puts = self.__process_data(new_puts, new_dates)

            # Save new data
            self.__save_data(new_processed_calls,self._calls_path,append=True)
            self.__save_data(new_processed_puts,self._puts_path,append=True)

            # Combine dataframes
            self._puts = pd.concat([self._puts, new_processed_puts])
            self._calls = pd.concat([self._calls, new_processed_calls])


    @property
    def calls(self):
        return_calls = self._calls[self._calls.index.get_level_values(0) >= self._start]
        return return_calls

    @property
    def puts(self):
        return_puts = self._puts[self._puts.index.get_level_values(0) >= self._start]
        return return_puts

    def _get_rec(self,symbol, printit=False):
        ticker = yf.Ticker(symbol)
        df = ticker.recommendations
        if printit:
            firms = df['Firm'].unique()
            to_grades = df['To Grade'].unique()
            from_grades = df['From Grade'].unique()
            actions = df['Action'].unique()
            space = "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ \n"
            for array in [firms, to_grades, from_grades, actions]:
                print(str(array) + space)
        return df

if __name__ == '__main__':
    optionHandler = Options("NFLX")
    optionHandler.puts
    optionHandler.calls
