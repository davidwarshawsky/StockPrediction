from src.data.Options import Options
import pytest
import pandas as pd

class TestInit(object):
    def test_none(self):
        optionsHandler = Options()
        actual_start_date = optionsHandler._start.strftime("%Y-%m-%d")
        default_start_date = '2010-01-01'
        start_message = 'Expected default start date: {}' \
                  'Actual start date: {}'
        assert  actual_start_date == default_start_date,start_message
        symbol_message = "Symbol should be None but is {} ".format(optionsHandler._symbol)
        assert optionsHandler._symbol is None, symbol_message

    def test_symbol(self):
        symbol = "GOOG"
        optionsHandler = Options(symbol)
        actual_start_date = optionsHandler._start.strftime("%Y-%m-%d")
        default_start_date = '2010-01-01'
        start_message = 'Expected default start date: {}' \
                        'Actual start date: {}'
        assert actual_start_date == default_start_date, start_message
        symbol_message = "Expected symbol {} Actual symbol {}".format(symbol,optionsHandler._symbol)
        assert optionsHandler._symbol == symbol, symbol_message

    def test_bad_symbol(self):
        symbol = "BADARGUMENT"
        with pytest.raises(ValueError) as exception_info:
            Options(symbol)
        expected_message = "{} is not a valid yfinance symbol".format(symbol)
        message = "{} expected error message not received".format(symbol)
        assert exception_info.match(expected_message),message

    def test_bad_date(self):
        symbol = "AMD"
        date = "20201-0-01"
        with pytest.raises(ValueError):
            Options(symbol,date)

    def test_bad_symbol_bad_date(self):
        symbol = "BADARGUMENT"
        date = "20201-0-01"
        with pytest.raises(ValueError):
            Options(symbol, date)


class TestSwitchStock(object):

    def test_default_to_normal(self):
        optionsHandler = Options()
        optionsHandler.switch_stock("GOOG")
        for x in [optionsHandler.calls,optionsHandler.puts]:
            column_names = list(x.columns)
            column_names.sort()
            expected_column_names = ['strike','lastPrice','bid','ask','change','percentChange','volume','openInterest',
                                     'impliedVolatility','inTheMoney']
            expected_column_names.sort()
            data_type = type(x)
            column_message = "Expected column names: <{}> Actual Column names <{}>".format(
                expected_column_names,
                column_names
            )
            type_message = "Expected data type: <pd.DataFrame()> Actual data type: {} ".format(
                data_type
                )
            # Test that the columns are equal to each other.
            assert sum([x==y for x,y in zip(column_names,expected_column_names)]) == len(expected_column_names), column_message
            # Test that the data has the correct type.
            assert data_type == pd.DataFrame, type_message

    def test_default_to_bad(self):
        optionsHandler = Options()
        with pytest.raises(ValueError):
            optionsHandler.switch_stock("BADARGUMENT")

    def test_normal_to_bad(self):
        optionsHandler = Options("GOOG")
        with pytest.raises(ValueError):
            optionsHandler.switch_stock("BADARGUMENT")

    def test_normal_to_normal(self):
        stocks = ["GOOG","NFLX"]
        optionsHandler = Options(stocks[0])
        first_path = optionsHandler._calls_path
        first_data = optionsHandler._calls.to_numpy()
        optionsHandler.switch_stock(stocks[1])

        symbol_message = "Expected symbol: <{}> Actual symbol: <{}>".format(stocks[1],optionsHandler._symbol)
        assert optionsHandler._symbol == stocks[1],symbol_message

        second_path = optionsHandler._calls_path
        path_message = "Expected path: <{}> Actual path: <{}>".format(first_path,second_path)
        assert first_path != second_path,path_message

        comparison = (first_data[:10][:10] == optionsHandler.calls.to_numpy()[:10][:10]).all()
        data_message = "Expected {} dataframe to be different than {} dataframe".format(stocks[0],stocks[1])
        assert not comparison,data_message

class TestSwitchStart(object):
    def test_default_to_normal(self):
        optionsHandler = Options()
        # Go back in time
        optionsHandler.switch_start("2005-01-01")
        expected_date = "2005-01-01"
        actual_date   = optionsHandler._start.strftime("%Y-%m-%d")
        message = "Date shouldn't be default, Expected: <{}> Actual: <{}>".format(
            expected_date,
            actual_date
        )
        assert expected_date == actual_date,message

    def test_default_to_bad(self):
        optionsHandler = Options()
        # Go back in time
        with pytest.raises(ValueError) as exception_info:
            optionsHandler.switch_start("20005-01-01")
        expected_message = "Incorrect data format, should be YYYY-MM-DD"
        message = "Validation of a new bad date failed"
        assert exception_info.match(expected_message),message

# def test_data():
if __name__ == "__main__":
    optionsHandler = Options()
    optionsHandler.switch_stock("GOOG")
    optionsHandler.switch_start("2020-07-24")
    data = optionsHandler.calls
    data_index_length = len(data.index)
    data_index_unique_length = len(data.index.unique())
    message = "Data index is not fully unique. Expected: <{}> Actual <{}>".format(
        data_index_length,
        data_index_unique_length
    )
    print(data.index[0])
    assert data_index_length == data_index_unique_length, message
