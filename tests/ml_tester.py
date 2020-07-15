import unittest
import sys
sys.path.append('appdata/stock_data/predictions/')
from src.models.prediction_maker import *
from src.models.prediction_tester import *
from datetime import timedelta

class MyTestCase(unittest.TestCase):
    # def test_wavenet(self):
    #     wn = WaveNet()
    #     self.assertEqual(True, False)

    def tests_symbols(self):
        self.assertEqual(len(read_invalid_symbols()),2)
        self.assertEqual(len(read_SP500_symbols()),503)

    def test_predictions(self):
        for data in split_data(Stock("AAPL")):
            self.assertEqual(len(data.shape),3)
            print(data.shape)
            for x in data.shape:
                self.assertGreaterEqual(x,1)

    def test_prediction_tester(self):
        days = 10
        pred_f_name = 'appdata/stock_data/predictions/wn&2020-08-11&10&20&5&100&1.csv'
        df,date = read_predictions(pred_f_name)
        # Makes sure that the test date is more than days(10) days ahead than the prediction date
        # for purposes of this test.
        self.assertFalse(valid_passed_days(date+timedelta(days=11),days))
        accuracy_dict = score_predictions(df, days)
        # Checks that score_predictions() function returns a dictionary
        self.assertIsInstance(accuracy_dict,dict())
        # Checks the length of the dictionary, the test case is meant for predictions of all SP500 stocks.
        self.assertEqual(len(accuracy_dict.values()),503)


if __name__ == '__main__':
    unittest.main()
