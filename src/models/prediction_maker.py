from src.data.dictionary import csv_to_dict, csv_to_list
from src.models.WaveNet import WaveNet
import pandas as pd
from src.data.Stock import Stock
# from src.features.TS import time_series_split
from src.models.modelFunctions import get_model_name
from datetime import date
import os

class ModelPredictorSP500():
    def read_invalid_symbols(self):
        invalid_path = '..{0}..{0}data{0}invalid_stocks.csv'.format(os.path.sep)
        with open(invalid_path) as invalid:
            return csv_to_list(invalid)


    def read_SP500_symbols(self):
        invalids = self.read_invalid_symbols()
        stock_path = '..{0}..{0}data{0}stocks.csv'.format(os.path.sep)
        with open(stock_path) as csv_file:
            dictionary = csv_to_dict(csv_file)
            return [x for x in list(dictionary) if x not in invalids]


    def make_prediction(self,stock: Stock):
        X_train, X_test, y_train, y_test, future_features = stock.split()
        wn = WaveNet(input_shape=(X_train.shape[1], X_train.shape[2]), epochs=1)
        history = wn.fit(X_train, y_train, X_test, y_test)
        return history,wn.predict(future_features)


    def make_SP500_preds(self):
        symbols = self.read_SP500_symbols()
        predictions_df = pd.DataFrame()
        history_df     = pd.DataFrame()

        stockHandler = Stock()
        for symbol in symbols:
            stockHandler.switch_stock(symbol)
            history,predictions = self.make_prediction(stockHandler)
            predictions_df[symbol] = [round(x[0][0], 3) for x in predictions]
            history_df[symbol] = history
        self.save_predictions(predictions_df)


    def save_predictions(df: pd.DataFrame):
        df.to_csv(
            "data{0}stock_data{0}predictions{0}".format(os.path.sep) + str(date.today()) + "&" + get_model_name().format("SP500") + ".csv")
