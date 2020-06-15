import yfinance as yf
import os
import sys
sys.path.append('..data/stock_data/recommendations/')
def get_options_dates(symbol):
    """
    Gets the dates available for options for a stock.
    :param symbol: The symbol of the stock.
    :return: A list of dates representing available otpion dates.
    """
    ticker = yf.Ticker(symbol)
    return list(ticker.options)

def get_option_chains(symbol,date):
    """
    Gets option chains for a stock.
    :param symbol: The symbol of the stock.
    :param date: The date or dates for the options chains.
    :return: A list of option chains
    """
    chains = []
    ticker = yf.Ticker(symbol)

    if type(date) == list:
        for d in date:
            chains.append(ticker.option_chain(d))

    if type(date) == str:
        chains.append(ticker.option_chain(date))

    return chains


def get_calls(chains):
    """
    Gets calls from option chains.
    :param chains: A list of option chains.
    :return: A list of calls as pandas Dataframes.
    """
    calls = []
    for chain in chains:
        calls.append(chain.calls)
    return calls

def get_puts(chains):
    """
    Gets puts fromp option chains.
    :param chains: A list of option chains.
    :return: A list of puts as pandas Dataframes.
    """
    puts = []
    for chain in chains:
        puts.append(chain.puts)
    return puts


def get_recs(ticker):
    df = ticker.recommendations
    firms       = df['Firm'].unique()
    to_grades   = df['To Grade'].unique()
    from_grades = df['From Grade'].unique()
    actions     = df['Action'].unique()
    space = "\n\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
    for array in [firms,to_grades,from_grades,actions]:
        print(str(array) + space)

# get_recs(yf.Ticker("AAPL"))
print(os.getcwd())
print(os.listdir())

if os.
firms = open('stock_data/recommendations/')