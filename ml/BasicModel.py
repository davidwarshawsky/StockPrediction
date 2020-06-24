from abc import ABC, abstractmethod


class BasicModel(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def plot_loss(self):
        pass

    @abstractmethod
    def build_model(self):
        pass

    @abstractmethod
    def save(self):
        pass
    @abstractmethod
    def load_model(self):
        pass