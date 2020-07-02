from ml.BasicModel import BaseModel
from data.TS import *
from data.Stock import Stock
from keras.models import Model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers import Input, Conv1D, Dense, Activation, Dropout, Lambda, Multiply, Add, Concatenate,Conv2D
from keras.optimizers import Adam
from data.Stock import Stock
from datetime import date
import os
import sys
from emailer import create_email,send_email
from ml.modelFunctions import get_model_name,set_model_name


# https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
# https://machinelearningmastery.com/convert-time-series-supervised-learning-problem-python/
# https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/

class WaveNet(BaseModel):
    def __init__(self, days=10, n_filters=20, filter_width=5, batch_size=2048, epochs=100):
        super().__init__()
        self.days = days
        self.filter_width = filter_width
        self.n_filters = n_filters
        self.batch_size = batch_size
        self.epochs = epochs

        # BUILDS THE MODEL
        n_filters = 20
        filter_width = 5
        dilation_rates = [2 ** i for i in range(7)] * 2

        # define an input history series and pass it through a stack of dilated causal convolution blocks
        history_seq = Input(shape=(self.X_train.shape[1], self.X_train.shape[2]))
        x = history_seq

        skips = []
        for dilation_rate in dilation_rates:
            # preprocessing - equivalent to time-distributed dense
            x = Conv1D(16, 1, padding='same', activation='relu')(x)

            # filter
            x_f = Conv1D(filters=self.n_filters,
                         kernel_size=self.filter_width,
                         padding='causal',
                         dilation_rate=dilation_rate)(x)

            # gate
            x_g = Conv1D(filters=self.n_filters,
                         kernel_size=self.filter_width,
                         padding='causal',
                         dilation_rate=dilation_rate)(x)

            # combine filter and gating branches
            z = Multiply()([Activation('tanh')(x_f),
                            Activation('sigmoid')(x_g)])

            # postprocessing - equivalent to time-distributed dense
            z = Conv1D(16, 1, padding='same', activation='relu')(z)

            # residual connection
            x = Add()([x, z])

            # collect skip connections
            skips.append(z)

        # add all skip connection outputs
        out = Activation('relu')(Add()(skips))

        # final time-distributed dense layers
        out = Conv1D(128, 1, padding='same')(out)
        out = Activation('relu')(out)
        out = Dropout(.2)(out)
        out = Conv1D(1, 1, padding='same')(out)

        # extract training target at end
        def slice(x, seq_length):
            return x[:, -seq_length:, :]

        pred_seq_train = Lambda(slice, arguments={'seq_length': 66})(out)

        model = Model(history_seq, pred_seq_train)
        model.compile(Adam(), loss='mean_absolute_error')
        self.model = model

    def fit(self,X_train,y_train,X_test,y_test):
        # Implement EarlyStopping and Keras Tuner later.
        # config = tf.compat.v1.ConfigProto()
        # config.gpu_options.allow_growth = True
        # with tf.device('/gpu:0'):
        return self.model.fit(X_train, y_train,batch_size=self.batch_size,epochs=self.epochs,validation_data=(X_test, y_test),shuffle=False)


    def save(self,symbol:str):
        model_json = self.model.to_json()
        # https://stackoverflow.com/questions/16084623/python-is-it-okay-to-pass-self-to-an-external-function
        model_name = set_model_name(self,symbol)
        with open(super().base_dir + model_name + ".json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights(super().base_dir + model_name + ".h5")

        
    def compile(self):
        self.model.compile(Adam(), loss='mean_absolute_error')
        print("Compiled model")



def main():
    # ??? https://machinelearningmastery.com/save-load-keras-deep-learning-models/
    aapl_stock = Stock("AAPL")
    X_train,y_train,X_test,y_test,future_features = time_series_split(aapl_stock.get_data())

    wn = WaveNet(epochs=100)
    model_name = get_model_name()
    wn.load_model(model_name,model_type='keras',load_weights=True)
    wn.compile()
    history = wn.fit(X_train,y_train,X_test,y_test)
    wn.plot_loss(history)
    predictions = wn.predict(future_features)



    message = "Microsoft 10 day percent change from " + day + ": " + pred
    email = create_email("AppliedMarkets Predictions MSFT!",message)
    send_email(email)

if __name__ == '__main__':
    main()