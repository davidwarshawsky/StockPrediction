from src.models.BaseModel import BaseModel
from keras.models import Model
from keras.layers import Input, Conv1D, Activation, Dropout, Lambda, Multiply, Add
from keras.optimizers import Adam
from src.models.modelFunctions import set_model_name


# https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
# https://machinelearningmastery.com/convert-time-series-supervised-learning-problem-python/
# https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/

class WaveNet(BaseModel):
    def __init__(self, input_shape:tuple,days=10, n_filters=20, filter_width=5, batch_size=1000, epochs=100):
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
        history_seq = Input(shape=input_shape)
        # self.X_train.shape[1], self.X_train.shape[2])
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
        return self.model.fit(X_train, y_train,batch_size=self.batch_size,
                              epochs=self.epochs,validation_data=(X_test, y_test),shuffle=False)


    def save(self,symbol:str):
        model_json = self.model.to_json()
        # https://stackoverflow.com/questions/16084623/python-is-it-okay-to-pass-self-to-an-external-function
        model_name = set_model_name(self,symbol)
        with open(super().base_dir + model_name + ".json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights(super().base_dir + model_name + ".h5")


