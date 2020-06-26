# File that defines functions for time series.
import pandas as pd
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	"""
	Frame a time series as a supervised learning dataset.
	Arguments:
		data: Sequence of observations as a list or NumPy array.
		n_in: Number of lag observations as input (X).
		n_out: Number of observations as output (y).
		dropnan: Boolean whether or not to drop rows with NaN values.
	Returns:
		Pandas DataFrame of series framed for supervised learning.
	"""
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg
def shifts(df, window):
    for col in df.columns.tolist():
        for i in range(1, window - 1):
            df[col + '_' + str(i)] = df[col].shift(-1 * i)
    replace_bad(df)
    return df

def holdout_confidence(real,pred,sample_weight = 0 ):
	"""provides accuracy dependant on the trend changes in a holdout set:
	   where class 1 is positive trend
	   and class 0 is negative trend"""
    pred = np.where(pred > 0 ,1,0)
    real = np.where(real > 0 ,1,0)
    return accuracy_score(real,pred)