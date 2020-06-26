import unittest
from ml.WaveNet import WaveNet

class MyTestCase(unittest.TestCase):
    def test_wavenet(self):
        wn = WaveNet()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
