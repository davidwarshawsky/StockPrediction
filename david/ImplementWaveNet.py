from WaveNet import *
from Stock import *

class WaveNetModel():
    stock = None
    def __init__(self,stock:Stock):
        self.stock = stock

    def save_model(self):
        pass

    def train_model(self):
        self.stock.get_stock_data()
        self.stock.update_data()
        X_train,X_test,y_train,y_test = self.stock.train_test_split()


    def get_accuracy(self):
        pass

