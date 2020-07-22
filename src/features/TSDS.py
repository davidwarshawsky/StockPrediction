# Stands for Time Series Data Structure
from abc import ABC, abstractmethod
from datetime import datetime

class TSDS(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def switch_stock(self):
        pass

    @abstractmethod
    def switch_start(self):
        pass

    @abstractmethod
    def __set_path(self):
        pass

    @abstractmethod
    def __set_symbol(self):
        pass

    @abstractmethod
    def get_start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def __retrieve_data(self) -> str:
        pass

    @abstractmethod
    def __update_data(self) -> bool:
        pass
    @abstractmethod
    def __process_data(self):
        pass
