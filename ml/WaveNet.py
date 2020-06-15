from ml.BasicModel import BasicModel
from data.TS import series_to_supervised
from data.Stock import Stock
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Conv1D, Dense, Activation, Dropout, Lambda, Multiply, Add, Concatenate,Conv2D
from keras.optimizers import Adam


# https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
# https://machinelearningmastery.com/convert-time-series-supervised-learning-problem-python/
# https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/

class WaveNet(BasicModel):
    def __init__(self, stock, days=10, n_filters=20, filter_width=5, batch_size=2048, epochs=100):
        self.stock = stock
        self.days = days
        self.stock.get_stock_data()
        self.stock.update_data()
        df = self.stock.get_data()
        df = df.drop(columns=['Volume'])
        # To scale data
        df = df.div(100)
        self.dates = df.index
        self.filter_width = filter_width
        self.n_filters = n_filters
        self.batch_size = batch_size
        self.epochs = epochs

        data_size = df.shape[0]
        copy = series_to_supervised(df.values, self.days, 1)
        copy = copy.drop(columns=['var1(t)', 'var2(t)', 'var3(t)', 'var4(t)'])
        values = copy.values

        values[:, -1] = pd.Series(values[:, -1].flatten()).pct_change(self.days).shift(-self.days).fillna(0).values
        train_size = int(values.shape[0] * 0.8)
        train = values[:train_size, :]
        test = values[train_size:, :]
        self.features_for_future = test[-self.days:, :-1]
        test = test[:-self.days]
        # split into input and outputs
        self.X_train, self.y_train = train[:, :-1], train[:, -1]
        self.X_test, self.y_test = test[:, :-1], test[:, -1]
        # reshape input to be 3D [samples, timesteps, features]
        self.X_train = self.X_train.reshape((self.X_train.shape[0], 1, self.X_train.shape[1]))
        self.X_test = self.X_test.reshape((self.X_test.shape[0], 1, self.X_test.shape[1]))
        self.y_train = self.y_train.reshape(self.y_train.shape[0], 1, 1)
        self.y_test = self.y_test.reshape(self.y_test.shape[0], 1, 1)

    def build_model(self):
        # hyper-parameters
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

    def fit(self):
        # Implement EarlyStopping and Keras Tuner later.
        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.device('/gpu:0'):
            self.history = self.model.fit(self.X_train, self.y_train,
                                          batch_size=self.batch_size,
                                          epochs=self.epochs,
                                          validation_data=(self.X_test, self.y_test),
                                          shuffle=False)

    def plot_loss(self):
        plt.plot(np.exp(self.history.history['loss']))
        plt.plot(np.exp(self.history.history['val_loss']))

        plt.xlabel('Epoch')
        plt.ylabel('Mean Absolute Error Loss')
        plt.title('Loss Over Time')
        plt.legend(['Train', 'Validation']);

    def predict(self):
        self.preds = self.model.predict(self.features_for_future.reshape(
            self.features_for_future.shape[0],
            1,
            self.features_for_future.shape[1]))
        self.report_df = pd.DataFrame(self.preds.reshape(self.features_for_future.shape[0], 1))
        return self.preds



    def get_last_days(self):
        return self.dates[-self.days:]

