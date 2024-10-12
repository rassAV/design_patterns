from abc import ABC, abstractmethod

class abstract_prototype(ABC):
    __data = []

    def __init__(self, source:list) -> None:
        super().__init__()
        self.__data = source

    @abstractmethod
    def create(self, data:list, filter):
        pass

    @property
    def data(self) -> list:
        return self.__data    
    
    @data.setter
    def data(self, value:list):
        self.__data = value