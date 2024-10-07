from src.core.abstract_model import abstract_model
from src.core.custom_raise import CustomRaise

class range(abstract_model):
    __unit_range: str = "грамм"
    __conversion_factor: int = 1
    __base_range: range = None

    def __init__(self, unit_range: str = "грамм", conversion_factor: int = 1, base_range: range = None):
        super().__init__()
        if base_range is not None:
            CustomRaise.value_required_exception(base_range.conversion_factor, conversion_factor)
        CustomRaise.type_exception("unit_range", unit_range, str)
        CustomRaise.type_exception("conversion_factor", conversion_factor, int)
        self.__unit_range = unit_range
        self.__conversion_factor = conversion_factor
        self.__base_range = base_range
    
    def __str__(self):
        return f"Range(unit: {self.unit_range}, factor: {self.conversion_factor})"

    @property
    def unit_range(self) -> str:
        return self.__unit_range
    
    @unit_range.setter
    def unit_range(self, unit_range: str):
        CustomRaise.type_exception("unit_range", unit_range, str)
        self.__unit_range = unit_range

    @property
    def conversion_factor(self) -> int:
        return self.__conversion_factor
    
    @conversion_factor.setter
    def conversion_factor(self, conversion_factor: int):
        CustomRaise.type_exception("conversion_factor", conversion_factor, int)
        self.__conversion_factor = conversion_factor

    @property
    def base_range(self) -> range:
        return self.__base_range
    
    @base_range.setter
    def base_range(self, base_range: range):
        CustomRaise.type_exception("base_range", base_range, range)
        self.__base_range = base_range

    @staticmethod
    def default_gram():
        return range()
    
    @staticmethod
    def default_kilogram():
        return range("килограмм", 1000, range()),
    
    @staticmethod
    def default_ton():
        return range("тонна", 1000, range("килограмм", 1000))
    
    def set_compare_mode(self, other) -> bool:
        if other is None or not isinstance(other, range): return False
        return self.name == other.name