from appdata.dictionary import csv_to_dict,csv_to_list
# from ml.WaveNet import WaveNet
import pandas as pd
# from appdata.Stock import Stock
# from appdata.TS import time_series_split
# from ml.modelFunctions import get_model_name,set_model_name
from datetime import date


def read_SP500_symbols():
    with open('appdata/stocks.csv') as csv_file:
        dictionary = csv_to_dict(csv_file)
        return list(dictionary)

def read_invalid_symbols():
    with open('appdata/invalid_stocks.csv') as invalid:
        return csv_to_list(invalid)

# def make_predictions(wn:WaveNet,stock:Stock,):
#     X_train, y_train, X_test, y_test, future_features = time_series_split(stock.get_data())
#     wn.compile()
#     wn.fit(X_train, y_train, X_test, y_test)
#     return wn.predict(future_features)
#
# def make_SP500_preds():
#     wn = WaveNet(epochs=10)
#     symbols = read_SP500_symbols()
#     df = pd.DataFrame()
#     stockHandler = Stock()
#     for symbol in symbols:
#         stockHandler.switch_stock(symbol)
#         predictions = make_predictions(wn,stockHandler,10)
#         df[symbol] = predictions
#     save_predictions(df)
#
# def save_predictions(df:pd.DataFrame,wn:WaveNet):
#     df.to_csv("appdata/predictions/" + str(date.today()) + "&" + set_model_name(wn,"SP500") + ".csv")
#



def main():
    print(read_SP500_symbols())

if __name__ == '__main__':
    main()


