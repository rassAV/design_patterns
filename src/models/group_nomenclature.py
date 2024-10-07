from src.core.abstract_model import abstract_model
from src.core.custom_raise import CustomRaise

class group_nomenclature(abstract_model):
    __name: str = ""

    def __init__(self, name: str = "default"):
        super().__init__()
        CustomRaise.type_exception("name", name, str)
        self.__name = name

    def __str__(self):
        return f"Group_nomenclature(name: {self.name})"

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name):
        CustomRaise.type_exception("name", name, str)
        self.__name = name

    @staticmethod
    def default_group_source():
        item = group_nomenclature()
        item.name = "Сырьё"
        return item
    
    @staticmethod
    def default_group_cold():
        item = group_nomenclature()
        item.name = "Заморозка"
        return item

    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)