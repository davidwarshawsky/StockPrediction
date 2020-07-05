from appdata.dictionary import csv_to_dict
from ml.WaveNet import WaveNet
import pandas as pd
from appdata.Stock import Stock
from appdata.TS import time_series_split
from ml.modelFunctions import get_model_name

def read_SP500_symbols():
    with open('appdata/stocks.csv') as csv_file:
        dictionary = csv_to_dict(csv_file)
        return list(dictionary)

def make_predictions(stock:Stock,days=10):
    X_train, y_train, X_test, y_test, future_features = time_series_split(stock.get_data())
    wn = WaveNet(epochs=10)
    wn.compile()
    wn.fit(X_train, y_train, X_test, y_test)
    return wn.predict(future_features)

def make_SP500_preds():
    symbols = read_SP500_symbols()
    df = pd.DataFrame()
    stockHandler = Stock()
    for symbol in symbols:
        stockHandler.switch_stock(symbol)
        predictions = make_predictions(stockHandler,10)
        df[symbol] = predictions




def main():

if __name__ == '__main__':
    main()


