from src.core.abstract_model import abstract_model
from src.core.custom_raise import CustomRaise
from src.models.nomenclature import nomenclature
from src.models.range import range
from src.models.storage import storage

class storage_turnover(abstract_model):
    __storage: storage = storage()
    __nomenclature: nomenclature = nomenclature()
    __range: range = range()
    __turnover: float = 0.0

    def __init__(self, strg: storage = storage(), nmcl: nomenclature = nomenclature(), rng: range = range(), turnover: float = 0.0):
        super().__init__()
        CustomRaise.type_exception("storage", strg, storage)
        CustomRaise.type_exception("nomenclature", nmcl, nomenclature)
        CustomRaise.type_exception("range", rng, range)
        CustomRaise.type_exception("turnover", turnover, float)
        self.__storage = strg
        self.__nomenclature = nmcl
        self.__range = rng
        self.__turnover = turnover
    
    def __str__(self):
        return f"Turnover(storage: {self.storage}, nomenclature: {self.nomenclature}, range: {self.range}, turnover: {self.turnover})"

    @property
    def storage(self) -> storage:
        return self.__storage

    @storage.setter
    def storage(self, value):
        CustomRaise.type_exception("storage", value, storage)
        self.__storage = value

    @property
    def nomenclature(self) -> nomenclature:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value):
        CustomRaise.type_exception("nomenclature", value, nomenclature)
        self.__nomenclature = value

    @property
    def range(self) -> range:
        return self.__range

    @range.setter
    def range(self, value):
        CustomRaise.type_exception("range", value, range)
        self.__range = value

    @property
    def turnover(self) -> float:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: float):
        self.__turnover = value

    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)