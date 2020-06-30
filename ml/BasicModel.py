from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
import pickle
from keras.models import Model, model_from_json
import sys
sys.path.append('ml/models/')
# FOR WAVENET TO RESHAPE DATA AFTER SERIES_TO_SUPERVISED
# self.preds = self.model.predict(pred_features.reshape(
#             self.pred_features.shape[0],
#             1,
#             self.pred_features.shape[1]))

class BaseModel(ABC):
    base_dir = 'ml/models/'

    def __init__(self,model=None):
        if model is not None:
            self.model = model

    def fit(self,X_train,y_train,X_val=None,y_val=None):
        """
        Fits a model.
        :param X_train: Features for training.
        :param y_train: Target for training.
        :param X_val: Validation features.
        :param y_val: Validation targets.
        :return: A plottable history object.
        """
        if X_val is not None and y_val is not None:
            return self.model.fit(X_train, y_train)
        elif X_val is not None and y_val is None or X_val is None and y_val is not None:
            raise ValueError("Missing either X_val or y_val ")
        else:
            return self.model.fit(X_train,y_train,validation_data=(X_val,y_val),shuffle=False)

    def predict(self,X_test):
        return self.model.predict(X_test)

    @staticmethod
    def plot_loss(self,history):
        plt.plot(np.exp(history.history['loss']))
        plt.plot(np.exp(history.history['val_loss']))

        plt.xlabel('Epoch')
        plt.ylabel('Mean Absolute Error Loss')
        plt.title('Loss Over Time')
        plt.legend(['Train', 'Validation'])
        plt.plot()

    @abstractmethod
    def save(self):
        pass

    def load_model(self,file_name='symbolicregressor5',model_type='pickle',load_weights=False):
        """
        Loads a model from file/s. Keras models require not adding the filepath
        :param file_name: The filename inside of ml/models/ without the file extension
        :param model_type: The type of model architecture to load from.
        :param load_weights: Whether to load weights for keras from h5 file.
        :return:
        """
        storage_types = ['pickle','keras']
        
        if model_type not in storage_types:
            raise ValueError("Not a valid model type to load")

        if model_type == 'pickle':
            with open(self.base_dir + file_name + '.pkl', 'rb') as f:
                self.model = pickle.load(f)
        elif model_type == 'keras':
            json_file = open(self.base_dir + file_name + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            self.model = model_from_json(loaded_model_json)
            if load_weights:
                self.model.load_weights(self.base_dir + file_name + ".h5")
                print("Loaded model from disk")

    def get_model(self):
        return self.model
