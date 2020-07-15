# Stands for Time Series Data Structure
from abc import ABC, abstractmethod
from datetime import datetime

class TSDS(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def set_target(self,target:str,start:str="2010-01-01"):
        """
        Sets parameters for the target to get.
        :param target: The stock symbol.
        :param start: The start of when to get data from.
        :return:
        """
        self.target = target
        self._switch_start(start)

    def _switch_start(self,start:str='2010-01-01'):
        """
        Internal function to change the start.
        :param start: The date of when to start getting data from.
        :return:
        """
        self.start = datetime.strptime(start, '%Y-%m-%d')

    @abstractmethod
    def set_filepath(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def _set_start(self):
        pass

    @abstractmethod
    def _set_stop(self):
        """
        An internal function to set the stop
        :return:
        """
        pass

    @abstractmethod
    def _update_data(self) -> bool:
        pass
