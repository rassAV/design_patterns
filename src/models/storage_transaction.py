from src.core.abstract_model import abstract_model
from src.core.custom_raise import CustomRaise
from src.models.nomenclature import nomenclature
from src.models.range import range
from src.models.storage import storage
from datetime import datetime
from src.core.object_types import transaction_type

class storage_transaction(abstract_model):
    __storage: storage = storage()
    __nomenclature: nomenclature = nomenclature()
    __range: range = range()
    __quantity: float = 0.0
    __period: datetime = datetime.now()
    __type: transaction_type = transaction_type.OUTCOME

    def __init__(self, strg: storage = storage(), nmcl: nomenclature = nomenclature(), rng: range = range(), qunt: float = 0.0, period: datetime = datetime.now(), type: transaction_type = transaction_type.OUTCOME):
        super().__init__()
        CustomRaise.type_exception("storage", strg, storage)
        CustomRaise.type_exception("nomenclature", nmcl, nomenclature)
        CustomRaise.type_exception("range", rng, range)
        if qunt <= 0:
            CustomRaise.operation_exception("Количество должно быть больше нуля!")
        CustomRaise.type_exception("period", period, datetime)
        CustomRaise.type_exception("transaction_type", type, transaction_type)
        self.__storage = strg
        self.__nomenclature = nmcl
        self.__range = rng
        self.__quantity = qunt
        self.__period = period
        self.__type = type
    
    def to_json(self):
        return {
            "id": self.id,
            "storage": self.storage.to_json(),
            "nomenclature": self.nomenclature.to_json(),
            "range": self.range.to_json(),
            "quantity": self.quantity,
            "period": self.period.isoformat(),
            "type": self.type.value,
        }
    
    @staticmethod
    def from_json(data):
        return storage_transaction(
            storage=storage.from_json(data.get("storage")),
            nomenclature=nomenclature.from_json(data.get("nomenclature")),
            range=range.from_json(data.get("range")),
            quantity=data.get("quantity"),
            period=datetime.fromisoformat(data.get("period")),
            type=transaction_type(data.get("type")),
        )

    def __str__(self):
        return f"Transaction(storage: {self.storage}, nomenclature: {self.nomenclature}, range: {self.range}, quantity: {self.quantity}, period: {self.period}, type: {self.type})"

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
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        if value <= 0:
            CustomRaise.operation_exception("Количество должно быть больше нуля!")
        self.__quantity = value

    @property
    def period(self) -> datetime:
        return self.__period

    @period.setter
    def period(self, value):
        CustomRaise.type_exception("period", value, datetime)
        self.__period = value

    @property
    def type(self) -> bool:
        return self.__type
    
    @type.setter
    def type(self, value: bool):
        CustomRaise.type_exception("transaction_type", value, transaction_type)
        self.__type = value

    @staticmethod
    def default_transaction_1():
        return storage_transaction(storage.default_storage_1(), nomenclature.default_nomenclature_1(), range.default_gram(), 200.0, datetime.now(), transaction_type.OUTCOME)

    @staticmethod
    def default_transaction_2():
        return storage_transaction(storage.default_storage_2(), nomenclature.default_nomenclature_2(), range.default_gram(), 150.0, datetime.now(), transaction_type.OUTCOME)

    @staticmethod
    def default_transaction_3():
        return storage_transaction(storage.default_storage_1(), nomenclature.default_nomenclature_1(), range.default_ton(), 1.25, datetime.now(), transaction_type.INCOME)

    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)