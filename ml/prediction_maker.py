import sys
import os
sys.path.append("C:\\Projects\\StockPrediction\\")
print(os.getcwd())
from appdata.dictionary import csv_to_dict

def read_SP500_symbols():
    with open('appdata/stocks.csv') as csv_file:
        dictionary = csv_to_dict(csv_file)
        print(dictionary.keys())
        print(len(dictionary.keys()))

read_SP500_symbols()