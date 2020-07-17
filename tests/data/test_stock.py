from src.data.Stock import Stock
from datetime import datetime
import pytest
class TestInit():
    def test_none(self):
        stockHandler = Stock()
        actual_start_date = stockHandler.start.strftime("%Y-%m-%d")
        default_start_date = '2010-01-01'
        start_message = 'Expected default start date: {}' \
                  'Actual start date: {}'
        assert  actual_start_date == default_start_date,start_message
        symbol_mesage = "Symbol should be None but is {} ".format(stockHandler.symbol)
        assert stockHandler.symbol == None, symbol_mesage

    def test_symbol(self):
        symbol = "GOOG"
        stockHandler = Stock(symbol)
        actual_start_date = stockHandler.start.strftime("%Y-%m-%d")
        default_start_date = '2010-01-01'
        start_message = 'Expected default start date: {}' \
                        'Actual start date: {}'
        assert actual_start_date == default_start_date, start_message
        symbol_mesage = "Expected symbol {} Actual symbol {}".format(symbol,stockHandler.symbol)
        assert stockHandler.symbol == symbol, symbol_mesage

    @pytest.mark.xfail
    def test_bad_symbol(self):
        symbol = "BADARGUMENT"
        with pytest.raises(ValueError) as exception_info:
            stockHandler = Stock(symbol)
        expected_message = "{} is not a valid yfinance symbol".format(symbol)
        message = "{} expected error message not received".format(symbol)
        assert exception_info == expected_message,message

    def test_bad_date(self):
        symbol = "AMD"
        date = "20201-0-01"
        with pytest.raises(ValueError) as exception_info:
            stockHandler = Stock(symbol,date)


        

        
