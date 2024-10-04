from src.core.custom_raise import CustomRaise
from abc import ABC, abstractmethod

import uuid

class abstract_model(ABC):
    __name = ""

    def __init__(self):
        self.__id = uuid.uuid1().hex

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        CustomRaise.type_exception("name", value, str)
        CustomRaise.length_exceeded_exception("name", value, 50)
        self.__name = value.strip()

    @abstractmethod
    def set_compare_mode(self, other_object) -> bool:
        if other_object is  None: return False
        if not isinstance(other_object, abstract_model): return False
        return self.__id == other_object.id
    
    def __eq__(self, value: object) -> bool:
        return self.set_compare_mode(value)