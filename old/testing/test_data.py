import unittest
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from data import Data

class DataTester(unittest.TestCase):

    def test_stock_getter(self):
        df_stocks = Data.get_SP500_stocks()
        self.assertEqual(df_stocks.shape[0], 505)

    def test_data_getter(self):
        data = Data(start='2010-01-01', stop='2020-01-01')
        X,y = data.retrieve_data('AAPL',60)
        self.assertEqual(X.shape[0],y.shape[0])


if __name__ == '__main__':
    unittest.main()
