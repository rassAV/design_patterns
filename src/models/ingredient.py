from src.core.abstract_model import abstract_model
from src.core.custom_raise import CustomRaise

class ingredient(abstract_model):
    __name: str = "default"
    __unit_value: int = 1
    __unit_name: str = ""

    def __init__(self, name: str = "default", unit_value: int = 1, unit_name: str = ""):
        CustomRaise.type_exception("name", name, str)
        CustomRaise.type_exception("unit_value", unit_value, int)
        CustomRaise.type_exception("unit_name", unit_name, str)
        self.__name = name
        self.__unit_value = unit_value
        self.__unit_name = unit_name

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        CustomRaise.type_exception("name", name, str)
        self.__name = name.strip()

    @property
    def unit_value(self) -> int:
        return self.__unit_value
    
    @unit_value.setter
    def unit_value(self, unit_value):
        CustomRaise.type_exception("unit_value", unit_value, int)
        self.__unit_value = unit_value

    @property
    def unit_name(self) -> str:
        return self.__unit_name
    
    @unit_name.setter
    def unit_name(self, unit_name):
        CustomRaise.type_exception("unit_name", unit_name, str)
        self.__unit_name = unit_name

    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)