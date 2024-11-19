from src.core.abstract_model import abstract_model
from src.core.custom_raise import CustomRaise

class storage(abstract_model):
    __name: str = ""
    __adress: str = ""

    def __init__(self, name: str = "default", adress: str = "default"):
        super().__init__()
        CustomRaise.type_exception("name", name, str)
        CustomRaise.type_exception("adress", adress, str)
        self.__name = name
        self.__adress = adress
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.adress,
        }
    
    @staticmethod
    def from_json(data):
        return storage(
            name=data.get("name"),
            address=data.get("address"),
        )

    def __str__(self):
        return f"Storage(name: {self.name}, factor: {self.adress})"

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name):
        CustomRaise.type_exception("name", name, str)
        self.__name = name

    @property
    def adress(self) -> str:
        return self.__adress
    
    @adress.setter
    def adress(self, adress):
        CustomRaise.type_exception("adress", adress, str)
        self.__adress = adress
    
    @staticmethod
    def default_storage_1():
        return storage("Default Storage 1", "Россия, г. Ангарск, кв-л. 71, 4")

    @staticmethod
    def default_storage_2():
        return storage("Default Storage 2", "Россия, г. Иркутск, ул. Советская, дом 22")

    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)