from src.models.BaseModel import BaseModel
from src.data.Stock import Stock
from src.data.Options import Options
from src.features.TS import series_to_supervised

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pandas as pd


class LSTM(BaseModel):
    def __init__(self,optionHandler:Options,stock:Stock,days=10):
        self.optionHandler = optionHandler
        self.stock = stock
        self.days = days

        self.puts,self.calls = self.optionHandler.get_puts_calls()

        self.puts = series_to_supervised(self.puts,self.days,1)
        self.calls = series_to_supervised(self.calls,self.days,1)

        target = self.stock.get_data()['Adj_Close']
        target = pd.Series(target).pct_change(self.days).shift(-self.days).fillna(0).values
        train_size = int(target.shape[0]  * 0.8)
        train_target = target.iloc[:train_size, :]
        test_target = target.iloc[train_size:, :]
        print(target[-20:])

    def _build_model(self,in_one_shapes:list,in_two_shapes:list):
        model1_inputs = tf.keras.Input(shape=(in_one_shapes[1],in_one_shapes[2]))
        model1_layer1 = tf.keras.layers.LSTM(16)(model1_inputs)
        # 21 classes
        model1_layer2 = tf.keras.layers.Dense(21, activation='softmax')(model1_layer1)

        model2_inputs = tf.keras.Input(shape=(in_two_shapes[1],in_two_shapes[2]))
        model2_layer1 = tf.keras.layers.LSTM(16)(model2_inputs)
        # 21 classes
        model2_layer2 = tf.keras.layers.Dense(21,activation='softmax')(model2_layer1)


        merged = tf.keras.layers.add([model1_layer1,model2_layer2])
        model = tf.keras.Model(inputs=[model1_inputs,model2_inputs],outputs=merged)
        model.compile('adam',loss='categorical_crossentropy',metrics=['accuracy'])
        self.model = model
        print(model.summary())


    def fit(self,X_train,y_train,X_test,y_test):
        self.history = self.model.fit(X_train,
                                      y_train,
                                      batch_size=self.batch_size,
                                      epochs=self.epochs,
                                      validation_data=(self.X_test, self.y_test),shuffle=False)

    def plot_loss(self):
        plt.plot(np.exp(self.history.history['loss']))
        plt.plot(np.exp(self.history.history['val_loss']))

        plt.xlabel('Epoch')
        plt.ylabel('Mean Absolute Error Loss')
        plt.title('Loss Over Time')
        plt.legend(['Train', 'Validation'])


    def predict(self):
        pass


    def save(self):
        pass
    def load_model(self):
        pass



def main():
    oh = Options("AAPL")
    stock = Stock("AAPL")
    lstm = LSTMOptions(oh,stock)

if __name__ == '__main__':
    main()
