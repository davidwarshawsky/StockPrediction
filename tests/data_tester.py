import unittest
from appdata import Stock,Options
from appdata.dictionary import *
import pandas as pd

class MyTestCase(unittest.TestCase):
    def test_stock_shape(self):
        aapl_stock = Stock("AAPL")
        aapl_data = aapl_stock.get_data()
        self.assertEqual(aapl_data.shape[1],6)

    def test_options_shape(self):
        aapl_options = Options("AAPL")
        puts,calls = aapl_options.get_puts_calls()
        self.assertEqual(puts.shape[1],calls.shape[1])

    def test_csv_rw(self):
        the_dict = csv_to_dict('..\\data\\stocks.csv')
        self.assertTrue( len(the_dict.keys()) >= 500)




if __name__ == '__main__':
    unittest.main()
