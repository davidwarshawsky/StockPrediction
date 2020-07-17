from src.data.Stock import Stock

class TestInit():
    def test_no_args(self):
        stockHandler = Stock()
        actual_start_date = stockHandler.start
        default_start_date = '2010-01-01'
        start_message = 'Expected default start date: {}' \
                  'Actual start date: {}'
        assert  actual_start_date == default_start_date,start_message
        symbol_mesage = "Symbol should be None but is {} ".format(stockHandler.symbol)
        assert stockHandler.symbol == None, symbol_mesage

    def test_symbol_arg(self):
        symbol = "GOOG"
        stockHandler = Stock(symbol)
        default_start_date = '2010-01-01'
        start_message = 'Expected default start date: {}' \
                        'Actual start date: {}'
        
