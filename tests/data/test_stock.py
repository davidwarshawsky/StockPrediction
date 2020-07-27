from src.data.Stock import Stock
from datetime import datetime
import pytest
import pandas as pd
import numpy as np


class TestInit(object):
    def test_none(self):
        stockHandler = Stock()
        actual_start_date = stockHandler._start.strftime("%Y-%m-%d")
        default_start_date = '2010-01-01'
        start_message = 'Expected default start date: {}' \
                  'Actual start date: {}'
        assert  actual_start_date == default_start_date,start_message
        symbol_message = "Symbol should be None but is {} ".format(stockHandler._symbol)
        assert stockHandler._symbol is None, symbol_message

    def test_symbol(self):
        symbol = "GOOG"
        stockHandler = Stock(symbol)
        actual_start_date = stockHandler._start.strftime("%Y-%m-%d")
        default_start_date = '2010-01-01'
        start_message = 'Expected default start date: {}' \
                        'Actual start date: {}'
        assert actual_start_date == default_start_date, start_message
        symbol_message = "Expected symbol {} Actual symbol {}".format(symbol,stockHandler._symbol)
        assert stockHandler._symbol == symbol, symbol_message

    def test_bad_symbol(self):
        symbol = "BADARGUMENT"
        with pytest.raises(ValueError) as exception_info:
            stockHandler = Stock(symbol)
        expected_message = "{} is not a valid yfinance symbol".format(symbol)
        message = "{} expected error message not received".format(symbol)
        assert exception_info.match(expected_message),message

    def test_bad_date(self):
        symbol = "AMD"
        date = "20201-0-01"
        with pytest.raises(ValueError):
            stockHandler = Stock(symbol,date)


class TestSwitchStock(object):

    def test_default_to_normal(self):
        stockHandler = Stock()
        stockHandler.switch_stock("GOOG")
        stock_data = stockHandler.data
        column_names = list(stock_data.columns)
        column_names.sort()
        expected_column_names = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
        expected_column_names.sort()
        stock_data_type = type(stock_data)

        column_message = "Expected column names: <{}> Actual Column names <{}>".format(
            expected_column_names,
            column_names
        )
        type_message = "Expected data type: <pd.DataFrame()> Actual data type: {} ".format(
            stock_data_type
            )
        # Test that the columns are equal to each other.
        assert sum([x==y for x,y in zip(column_names,expected_column_names)]) == len(expected_column_names), column_message
        # Test that the data has the correct type.
        assert stock_data_type == pd.DataFrame, type_message

    def test_default_to_bad(self):
        stockHandler = Stock()
        with pytest.raises(ValueError):
            stockHandler.switch_stock("BADARGUMENT")

    def test_normal_to_bad(self):
        stockHandler = Stock("GOOG")
        with pytest.raises(ValueError):
            stockHandler.switch_stock("BADARGUMENT")

    def test_normal_to_normal(self):
        stocks = ["GOOG","NFLX"]
        stockHandler = Stock(stocks[0])
        first_path = stockHandler._path
        first_data = stockHandler.data.to_numpy()
        stockHandler.switch_stock(stocks[1])

        symbol_message = "Expected symbol: <{}> Actual symbol: <{}>".format(stocks[1],stockHandler._symbol)
        assert stockHandler._symbol == stocks[1],symbol_message

        second_path = stockHandler._path
        path_message = "Expected path: <{}> Actual path: <{}>".format(first_path,second_path)
        assert first_path != second_path,path_message

        comparison = first_data != stockHandler.data.to_numpy()
        data_message = "Expected {} dataframe to be different than {} dataframe".format(stocks[0],stocks[1])
        assert comparison.all(),data_message

class TestSwitchStart(object):
    def test_normal_to_normal(self):
        stockHandler = Stock("AAPL")
        # Go back in time
        stockHandler.switch_start("2005-01-01")
        expected_date = "2010-01-01"
        actual_date   = stockHandler._start.strftime("%Y-%m-%d")
        message = "Date shouldn't be default, Expected: <{}> Actual: <{}".format(
            expected_date,
            actual_date
        )
        assert expected_date != actual_date,message

    def test_normal_to_bad(self):
        stockHandler = Stock("GOOGL")
        # Go back in time
        with pytest.raises(ValueError) as exception_info:
            stockHandler.switch_start("20005-01-01")
        expected_message = "Incorrect data format, should be YYYY-MM-DD"
        message = "Validation of a new bad date failed"
        assert exception_info.match(expected_message),message

# def test_data():
if __name__ == "__main__":
    stockHandler = Stock("LPCN")
    data = stockHandler.data
    data_index_length = len(data.index)
    data_index_unique_length = len(data.index.unique())
    message = "Data index is not fully unique. Expected: <{}> Actual <{}>".format(
        data_index_length,
        data_index_unique_length
    )
    print(data.index[0])
    assert data_index_length == data_index_unique_length, message





        

        
