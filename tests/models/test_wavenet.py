from src.models.WaveNet import WaveNet
from src.models.modelFunctions import set_model_name
import numpy as np
import pytest
import os

class TestWaveNet(object):
   def test_compile(self):
       wn = WaveNet(input_shape=(1, 6), epochs=1)
       message = 'Wavenet has not been compiled'
       assert wn is not None,message
       return wn

   def test_fit(self):
       wn = self.test_compile()
       message = 'Wavenet has not been compiled'
       assert wn is not None, message
       X_train, y_train, X_test, y_test = np.zeros((80,1,6)),np.zeros((80,1,1)),np.zeros((20,1,6)),np.zeros((20,1,1))
       wn.fit(X_train, y_train, X_test, y_test)
       message = 'Wavenet has not been fit successfully'
       assert wn is not None, message
       del(X_train, y_train, X_test, y_test)
       return wn

   def test_predict(self):
       wn = self.test_fit()
       preds = wn.predict(np.zeros((20, 1, 6)))
       message = 'Wavenet has not predicted successfully'
       assert preds is not None, message
       del(preds)

   @pytest.mark.fixture
   def test_save(self,tmpdir):
       wn = self.test_fit()
       # Use the appropriate method to create a file in the temporary directory

       model_json = wn.model.to_json()
       model_name = 'TEST'

       tmpdir.join(model_name + ".json").mkdir()
       tmpdir.join(model_name + ".h5").mkdir()

       with open(str(tmpdir) + model_name + ".json", "w") as json_file:
           json_file.write(model_json)
       # serialize weights to HDF5
       wn.model.save_weights(str(tmpdir) + model_name + ".h5")
       expected = 2
       message = "Files did not correctly get written to the temporary directory. Expected {} files, not {} files"
       assert len(os.listdir(tmpdir)) == 2, message.format(expected,len(os.listdir(tmpdir)))