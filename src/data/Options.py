import yfinance as yf
import pandas as pd
import os
import sys
import numpy as np
from datetime import datetime
sys.path.append('appdata/stock_data/recommendations/')
from src.features.TSDS import TSDS
from src.features.TS import validate

# https://github.com/mcdallas/wallstreet

class Option(TSDS):
    """
    A stock data structure to hold stock data
    """
    _puts: pd.DataFrame
    _calls: pd.DataFrame
    _symbol: str
    _ticker: yf.Ticker
    _puts_path  = None
    _calls_path = None
    _dates      = None

    def __init__(self,symbol:str=None,start:str='2010-01-01'):
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
        # Format the filepath
        puts_path = "appdata/stock_data/options/p{}.csv"
        calls_path = "appdata/stock_data/options/c{}.csv"
        self._puts_path = puts_path.format(self._symbol)
        self._calls_path = calls_path.format(self._symbol)

    def __retrieve_data(self):
        """
        Retrieves puts and calls dataframes from csv.
        :return:
        """

        def __retrieve_data(self):
            # check if data is already available
            if os.path.isfile(self._calls_path) and os.path.isfile(self._puts_path):
                # Read in all data and select a subset based on the start in case last time
                # the Stock was called an earlier start date was used.
                self._puts = pd.read_csv(self._puts_path, index_col=[0, 1])
                self._calls = pd.read_csv(self._calls_path, index_col=[0, 1])
                self._dates = list(self._puts.index.get_level_values(0).unique())
                return "r"
            else:
                # Load & Select ALL Data, you don't get a choice.
                # You get to choose a subsection of ALL THE DATA.
                data = yf.download(self._symbol, rounding=True)
                self._all_data = self.__process_data(data)
                # Save the data for later.
                self.__save_data(self._all_data, append=False)
                # Return
                return "w"

    def __pull_data(self):
        print("GETTING FRESH")
        self._set_puts_calls()
        self.puts, self.calls = self.__get_calls_puts()
        # Save data for later
        self._puts.to_csv(self.puts_filepath)
        self._calls.to_csv(self.calls_filepath)

    def __set_puts_calls(self):
        # Getting chains
        dates  = self.__get_options_dates(self.ticker)
        chains = self._get_option_chains(self.ticker,dates)
        #Setting
        self._puts = self._process_data(self._get_puts(chains),dates)
        self._calls  = self._process_data(self._get_calls(chains),dates)

    def __get_calls_puts(self):
        return self.puts,self.calls


    def __get_options_dates(self,ticker):
        """
        Gets the dates available for options for a stock.
        """
        return list(ticker.options)

    def __get_option_chains(self,ticker,date):
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
        return df


    def __update_data(self):
        # Get all available dates for options
        new_dates = self.__get_options_dates(self.ticker)
        # If there are new dates available for options, select them.
        if self._dates != new_dates:
            # Get dates to update
            new_dates = [x for x in new_dates if x not in self.dates]
            # Add new dates to dates
            self.dates = self._dates.append(new_dates)
            # Get new options and process them
            new_chains = self._get_option_chains(self.ticker, dates_to_update)
            new_puts = self._get_puts(new_chains)
            new_calls = self._get_calls(new_chains)
            new_puts.to_csv(self.puts_filepath, mode="a", headers=False)
            new_calls.to_csv(self.calls_filepath, mode="a", headers=False)
            dfn_puts = self.__process_data(new_puts, new_dates)
            dfn_calls = self.__process_data(new_calls, new_dates)
            # Combine dataframes
            self.puts = pd.concat([self.puts, dfn_puts])
            self.calls = pd.concat([self.calls, dfn_calls])

    def _get_rec(symbol, printit=False):
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