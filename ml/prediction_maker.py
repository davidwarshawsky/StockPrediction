from appdata.dictionary import csv_to_dict,csv_to_list
from ml.WaveNet import WaveNet
import pandas as pd
from appdata.Stock import Stock
from appdata.TS import time_series_split
from ml.modelFunctions import get_model_name,set_model_name
from datetime import date


def read_SP500_symbols():
    invalids = read_invalid_symbols()
    with open('appdata/stocks.csv') as csv_file:
        dictionary = csv_to_dict(csv_file)
        return [x for x in list(dictionary) if x not in invalids]

def read_invalid_symbols():
    with open('appdata/invalid_stocks.csv') as invalid:
        return csv_to_list(invalid)

def split_data(stock:Stock):
    df = stock.get_data()
    print("split data" , df.shape)
    return time_series_split(df,10)

def make_predictions(stock:Stock):
    X_train, y_train, X_test, y_test, future_features = split_data(stock)

    wn = WaveNet(input_shape=(X_train.shape[1],X_train.shape[2]), epochs=1)
    wn.fit(X_train, y_train, X_test, y_test)
    return wn.predict(future_features)

def make_one_pred(symbol):
    stockHandler = Stock(symbol)
    X_train, y_train, X_test, y_test, future_features = split_data(stockHandler)
    for x in [X_train,y_train,X_test,y_test,future_features]:
        print("make one pred" , x.shape)
    wn = WaveNet(input_shape=(X_train.shape[1], X_train.shape[2]), epochs=1)
    wn.fit(X_train, y_train, X_test, y_test)
    return wn.predict(future_features)

def make_SP500_preds():
    symbols = read_SP500_symbols()
    df = pd.DataFrame()
    stockHandler = Stock()
    for symbol in ['LNT']:
        stockHandler.switch_stock(symbol)
        predictions = make_predictions(stockHandler)
        df[symbol] = [x[0][0] for x in predictions]
    save_predictions(df)

def save_predictions(df:pd.DataFrame):
    df.to_csv("appdata/stock_data/predictions/" + str(date.today()) + "&" + get_model_name().format("SP500") + ".csv")




def main():
    # X_train, y_train, X_test, y_test, future_features = split_data(Stock("AAPL"))
    print(make_one_pred("HPE"))


if __name__ == '__main__':
    main()


