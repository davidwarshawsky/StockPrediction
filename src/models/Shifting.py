import pickle
import sys
sys.path.append('ml/models/')
sys.path.append('data/stock_data/predictions/')
from gplearn.genetic import SymbolicRegressor
from src.models.BaseModel import BaseModel

class SymbolicRegressor(BaseModel):

    def __init__(self):
        super(SymbolicRegressor(stopping_criteria=5))

    def save(self):
        with open('ml/models/symbolicregressor5.pkl', 'wb') as f:
            pickle.dump(self.symR, f)


    def load_model(self):
        with open('ml/models/symbolicregressor5.pkl', 'rb') as f:
            self.symR = pickle.load(f)
            # Error allowed to each sample.


# from data.TS import shifts

def main():
    # send_email("davidawarshawsky@gmail.com", "Come on hear me out", message)
    pass

if __name__ == '__main__':
    main()