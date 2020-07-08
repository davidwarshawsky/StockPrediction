import unittest
from ml.WaveNet import WaveNet
from ml.prediction_maker import *

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

if __name__ == '__main__':
    unittest.main()
