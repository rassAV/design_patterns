from src.core.abstract_model import abstract_model
from src.models.range import range
from src.models.group_nomenclature import group_nomenclature
from src.core.custom_raise import CustomRaise

class nomenclature(abstract_model):
    __full_name: str = "default"
    __group: group_nomenclature = group_nomenclature()
    __range: range = range()

    def __init__(self, full_name: str = "default", group: group_nomenclature = group_nomenclature(), rng: range = range()):
        super().__init__()
        CustomRaise.type_exception("full_name", full_name, str)
        CustomRaise.length_exceeded_exception("full_name", full_name, 255)
        CustomRaise.type_exception("group_nomenclature", group, group_nomenclature)
        CustomRaise.type_exception("range", rng, range)
        self.__full_name = full_name
        self.__group = group
        self.__range = rng

    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @full_name.setter
    def full_name(self, full_name: str):
        CustomRaise.type_exception("full_name", full_name, str)
        CustomRaise.length_exceeded_exception("full_name", full_name, 255)
        self.__full_name = full_name.strip()

    @property
    def group_nomenclature(self) -> group_nomenclature:
        return self.__group
    
    @group_nomenclature.setter
    def group_nomenclature(self, group):
        CustomRaise.type_exception("group_nomenclature", group, group_nomenclature)
        self.__group = group

    @property
    def range(self) -> range:
        return self.__range
    
    @range.setter
    def range(self, rng):
        CustomRaise.type_exception("range", rng, range)
        self.__range = rng
    
    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)