import pandas as pd
import numpy as np
from Stock import *

from keras.models import Model
from keras.layers import Input, Conv1D, Dense, Activation, Dropout, Lambda, Multiply, Add, Concatenate
from keras.optimizers import Adam




# hyper-parameters
n_filters = 32
filter_width = 2
dilation_rates = [2 ** i for i in range(7)] * 2

# define an input history series and pass it through a stack of dilated causal convolution blocks
history_seq = Input(shape=(None, 1))
x = history_seq

skips = []
for dilation_rate in dilation_rates:
    # preprocessing - equivalent to time-distributed dense
    x = Conv1D(16, 1, padding='same', activation='relu')(x)

    # filter
    x_f = Conv1D(filters=n_filters,
                 kernel_size=filter_width,
                 padding='causal',
                 dilation_rate=dilation_rate)(x)

    # gate
    x_g = Conv1D(filters=n_filters,
                 kernel_size=filter_width,
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



# Pred Seq Train would be the predictions
model = Model(history_seq, out)
model.compile(Adam(), loss='mean_absolute_error')

