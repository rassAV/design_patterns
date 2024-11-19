from src.core.abstract_model import abstract_model
from src.models.range import range
from src.models.nomenclature import nomenclature
from src.core.custom_raise import CustomRaise

class ingredient(abstract_model):
    __name: str = "default"
    __unit_value: int = 1
    __range: range = range()
    __nomenclature: nomenclature = nomenclature()

    def __init__(self, name: str = "default", unit_value: int = 1, rng: range = range(), product: nomenclature = nomenclature()):
        super().__init__()
        CustomRaise.type_exception("name", name, str)
        CustomRaise.type_exception("unit_value", unit_value, int)
        CustomRaise.type_exception("range", rng, range)
        CustomRaise.type_exception("nomenclature", product, nomenclature)
        self.__name = name
        self.__unit_value = unit_value
        self.__range = rng
        self.__nomenclature = product

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "unit_value": self.unit_value,
            "range": self.range.to_json(),
            "nomenclature": self.nomenclature.to_json(),
        }
    
    @staticmethod
    def from_json(data):
        return ingredient(
            name=data.get("name"),
            unit_value=data.get("unit_value"),
            range=range.from_json(data.get("range")),
            nomenclature=nomenclature.from_json(data.get("nomenclature")),
        )

    def __str__(self):
        return f"Ingredient(name: {self.name}, unit_value: {self.unit_value}, range: {str(self.range)}, nomenclature: {str(self.nomenclature)})"

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
    def range(self) -> range:
        return self.__range
    
    @range.setter
    def range(self, rng):
        CustomRaise.type_exception("range", rng, range)
        self.__range = rng

    @property
    def nomenclature(self) -> nomenclature:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, product):
        CustomRaise.type_exception("nomenclature", product, nomenclature)
        self.__nomenclature = product

    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)