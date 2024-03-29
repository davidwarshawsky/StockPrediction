from src.data.dictionary import csv_to_dict, csv_to_list
from src.models.WaveNet import WaveNet
import pandas as pd
# from src.features.TS import time_series_split
from src.models.modelFunctions import create_model_name
from datetime import date
import os

class ModelPredictorSP500():
    prediction_df = None
    history_df    = None
    base_dir      = "data{0}stock_data{0}predictions{0}"
    model_description = str(date.today()) + "&10&20&5&1000&100"
    history       = None

    @staticmethod
    def read_invalid_symbols():
        invalid_path = 'data{0}invalid_stocks.csv'.format(os.path.sep)
        with open(invalid_path) as invalid:
            return csv_to_list(invalid)

    @staticmethod
    def read_SP500_symbols():
        invalids = ModelPredictorSP500.read_invalid_symbols()
        stock_path = 'data{0}stocks.csv'.format(os.path.sep)
        with open(stock_path) as csv_file:
            dictionary = csv_to_dict(csv_file)
            return [x for x in list(dictionary) if x not in invalids]


    def make_prediction(self,X_train,X_test,y_train,y_test,future_features):
        wn = WaveNet(input_shape=(X_train.shape[1], X_train.shape[2]), epochs=2)
        wn.fit(X_train, y_train, X_test, y_test)
        return wn,wn.predict(future_features)


    def make_multiple_preds(self,symbols):
        # DataFrames for results
        self.prediction_df = pd.DataFrame()
        self.history_df = pd.DataFrame()
        from src.data.Stock import Stock
        stockHandler = Stock()
        i=1
        symbols_len = len(symbols)
        for symbol in symbols:
            stockHandler.switch_stock(symbol)
            X = stockHandler._all_data
            y = stockHandler.create_target(X, window=10)
            X_train, X_test, y_train, y_test, future_features = stockHandler.split(X, y, transpose=True, window=10)
            history,predictions = self.make_prediction(X_train, X_test, y_train, y_test, future_features)
            self.prediction_df[symbol] = [round(x[0][0], 3) for x in predictions]
            self.history_df[symbol + '_loss'] = history.loss()
            self.history_df[symbol + '_val_loss'] = history.val_loss()
            print(type(history))
            self.save_df(self.prediction_df,"sp500preds")
            if i % 10 == 0:
                print("{} / {}".format(i,symbols_len))
            i = i + 1
        self.save_df(self.history_df,'history')
        html = self.prediction_df.to_html()
        prediction_file = open(self.base_dir.format(os.path.sep) + "predictions.html")
        prediction_file.write(html)
        prediction_file.close()



    def save_df(self,df: pd.DataFrame,label):
        df.to_csv(
            self.base_dir.format(os.path.sep)
            + label + self.model_description + ".csv"
        )

def main():
    modelPredictor = ModelPredictorSP500()
    symbols = ModelPredictorSP500().read_SP500_symbols()[:2]
    modelPredictor.make_multiple_preds(symbols)


if __name__ == '__main__':
    main()
