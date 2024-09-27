from abc import ABC, abstractmethod
from src.core.format_reporting import format_reporting
from src.core.custom_raise import CustomRaise

class abstract_report(ABC):
    __format: format_reporting = format_reporting.CSV
    __result: str = ""

    @abstractmethod
    def create(self, data: list):
        pass

    @abstractmethod
    def save(self, directory: str, filename: str):
        pass

    @property
    def format(self) -> format_reporting:
        return self.__format
    
    @property
    def result(self) -> str:
        return self.__result
    
    @result.setter
    def result(self, value: str):
        CustomRaise.type_exception("data", value, str)
        self.__result = value