from ml.BasicModel import BasicModel
from data.Options import *
from data.TS import series_to_supervised
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.layers import LSTM,Dense,Dropout,Input

optionsHandler = Options("AAPL")

class LSTMOptions(BasicModel):
    def __init__(self,optionHandler:Options):
        self.optionHandler = optionHandler

    def fit(self):
        self.history = self.model.fit(self.X_train,
                                      self.y_train,
                                      batch_size=self.batch_size,
                                      epochs=self.epochs,
                                      validation_data=(self.X_test, self.y_test),shuffle=False)

    def predict(self):
        pass

    def plot_loss(self):
        plt.plot(np.exp(self.history.history['loss']))
        plt.plot(np.exp(self.history.history['val_loss']))

        plt.xlabel('Epoch')
        plt.ylabel('Mean Absolute Error Loss')
        plt.title('Loss Over Time')
        plt.legend(['Train', 'Validation'])


    def build_model(self):
        model1_inputs = tf.keras.Input(shape=(11,))
        model1_layer1 = tf.keras.layers.LSTM(16)(model1_inputs)
        # 21 classes
        model1_layer2 = tf.keras.layers.Dense(21, activation='softmax')(model1_layer1)

        model2_inputs = tf.keras.Input(shape=(11,))
        model2_layer1 = tf.keras.layers.LSTM(16)(model2_inputs)
        # 21 classes
        model2_layer2 = tf.keras.layers.Dense(21,activation='softmax')(model2_layer1)


        merged = tf.keras.layers.add([model1_layer1,model2_layer2])
        model = tf.keras.Model(inputs=[model1_inputs,model2_inputs],outputs=merged)
        model.compile('adam',loss='categorical_crossentropy',metrics=['accuracy'])


    def build_model(self):
        puts_inputs,calls_inputs = self.optionHandler.set_puts_calls()

        # m1 =


        model = Model(inputs=[puts_inputs,calls_inputs])
        print(model.summary())

        return model




