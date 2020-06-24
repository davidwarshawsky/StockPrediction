import yfinance as yf
import pandas as pd
import os
import sys
import numpy as np
from data.TS import series_to_supervised
sys.path.append('data/stock_data/recommendations/')


# https://github.com/mcdallas/wallstreet

class Options():
    puts:pd.DataFrame
    calls:pd.DataFrame
    symbol:str
    def __init__(self, symbol):
        self.switch_stock(symbol)

    def switch_stock(self,symbol):
        self.symbol = symbol
        self.ticker = yf.Ticker(self.symbol)
        self._set_filepath()
        # If you already have some puts and calls read them in from CSV
        if os.path.exists(self.puts_filepath) and os.path.exists(self.calls_filepath):
            self._retrieve_data()
        # If the options haven not been read in before
        else:
            self._pull_data()

    def _retrieve_data(self):
        print("RETRIEVING DATA FROM CSV")
        self.puts = pd.read_csv(self.puts_filepath,index_col=[0,1])
        self.calls = pd.read_csv(self.calls_filepath,index_col=[0,1])

        self.dates = list(self.puts.index.get_level_values(0).unique())
        print(self.puts.shape, self.calls.shape)

    def _pull_data(self):
        print("GETTING FRESH")
        self._set_puts_calls()
        self.puts, self.calls = self.get_puts_calls()
        # Save data for later
        self.puts.to_csv(self.puts_filepath)
        self.calls.to_csv(self.calls_filepath)
        print(self.puts.shape, self.calls.shape)

    def _update(self):
        # Get all available dates for options
        new_dates = self._get_options_dates(self.ticker)
        # If there are new dates available for options, select them.
        if self.dates != new_dates:
            # Get dates to update
            dates_to_update = [x for x in new_dates if x not in self.dates]
            # Add new dates to dates
            self.dates = self.dates + dates_to_update
            # Get new options and process them
            new_chains = self._get_option_chains(self.ticker,dates_to_update)
            new_puts   = self._get_puts(new_chains)
            new_calls  = self._get_calls(new_chains)
            new_puts.to_csv(self.puts_filepath,mode="a",headers=False)
            new_calls.to_csv(self.calls_filepath,mode="a",headers=False)
            dfn_puts   = self._process_options(new_puts,new_dates)
            dfn_calls  = self._process_options(new_calls,new_dates)
            # Combine dataframes
            self.puts  = pd.concat([self.puts,dfn_puts])
            self.calls = pd.concat([self.calls,dfn_calls])

    def _set_filepath(self):
        # Format the filepath
        puts_filepath = "data/stock_data/options/p{}.csv"
        calls_filepath = "data/stock_data/options/c{}.csv"
        self.puts_filepath  = puts_filepath.format(self.symbol)
        self.calls_filepath = calls_filepath.format(self.symbol)

    def _set_puts_calls(self):
        # Getting chains
        dates  = self._get_options_dates(self.ticker)
        chains = self._get_option_chains(self.ticker,dates)
        #Setting
        self.puts = self._process_options(self._get_puts(chains),dates)
        self.calls  = self._process_options(self._get_calls(chains),dates)

    def get_puts_calls(self):
        return self.puts,self.calls


    def _get_options_dates(self,ticker):
        """
        Gets the dates available for options for a stock.
        """
        return list(ticker.options)

    def _get_option_chains(self,ticker,date):
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

    def _get_calls(self,chains):
        """
        Gets calls from option chains..
        """
        calls = []
        for chain in chains:
            calls.append(chain.calls)
        return calls

    def _get_puts(self,chains):
        """
        Gets puts from option chains.
        """
        puts = []
        for chain in chains:
            puts.append(chain.puts)
        return puts

    def _process_options(self,df, dates):
        df = pd.concat(df, keys=dict(zip(dates, df)))
        df['inTheMoney'] = df['inTheMoney'].replace({False: 0, True: 1})
        df['inTheMoney'] = df['inTheMoney'].astype(np.bool)
        df['impliedVolatility'] = df['impliedVolatility'].astype(np.int32)
        df = df.drop(columns=['lastTradeDate','contractSymbol', 'contractSize', 'currency'])
        df = df.round(2)
        return df

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


def main():
    optionsHandler = Options("AMD")
    puts,calls = optionsHandler.get_puts_calls()
    print(puts.columns,puts.dtypes)
    print(puts.head())
    # df_puts = series_to_supervised(puts,10,1)
    # print(df_puts.info(),df_puts.shape,df_puts.columns)


if __name__ == '__main__':
    main()
