from sklearn.metrics import mean_absolute_error,accuracy_score
import numpy as np

class FeatureGenerator():
    @staticmethod
    def GAP_LAP(X,windows=[1,2,5,10]):
        """
        Calculates gap lap.
        Taken from Stock.ipynb
        :param X:
        :param windows:
        :return:
        """
        for window in windows:
            X['GapUp_'+str(window)] = (X['Open'].shift(-window).fillna(value = 0) > X['High']).astype(int)
            X['LapUp_'+str(window)] = (X['Open'].shift(-window).fillna(value = 0) > X['Adj_Close']).astype(int)
            X['GapUp_Sum_'+str(window)] = (X['GapUp_'+str(window)].rolling(5).aggregate(lambda x : x.sum()))
            X['LapUp_Sum_'+str(window)] = (X['LapUp_'+str(window)].rolling(5).aggregate(lambda x : x.sum()))
        return X

    @staticmethod
    def comparitive_stds(X, windows=[10]):
        """
        Calculates comparitive standard deviations.
        Taken from Stock.ipynb
        :param windows:
        :return:
        """
        for window in windows:
            base = X['Open', 'High', 'Low'].mean(axis=0)
            local_means = base.rolling(window).mean()[::window].tolist()
            for mean in local_means:
                local_groups = np.array_split(base, window)
    @staticmethod
    def categorical(pred, real):
        pred = np.where(pred > 0, 1, 0)
        real = np.where(real > 0, 1, 0)
        return accuracy_score(real, pred)
    @staticmethod
    def apply_shifts(df, window=10):
        for col in df.columns.tolist():
            for i in range(1, window):
                df[col + '_' + str(i)] = df[col].shift(-1 * i)
        return df