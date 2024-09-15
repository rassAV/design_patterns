from src.abstract_model import abstract_model
from src.models.range import range
from src.models.group_nomenclature import group_nomenclature
from src.custom_raise import CustomRaise

class nomenclature(abstract_model):
    __full_name: str = ""
    __group_nomenclature: group_nomenclature = group_nomenclature()
    __range: range = range()

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
        return self.__group_nomenclature
    
    @group_nomenclature.setter
    def group_nomenclature(self, group_nomenclature):
        self.__group_nomenclature = group_nomenclature

    @property
    def range(self) -> range:
        return self.__range
    
    @range.setter
    def range(self, range):
        self.__range = range
    
    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)