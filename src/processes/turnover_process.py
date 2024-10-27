from src.models.storage_turnover import storage_turnover
from src.core.abstract_logic import abstract_logic
from src.core.object_types import transaction_type
from datetime import datetime
from src.core.custom_raise import CustomRaise

class turnover_process(abstract_logic):
    __start: datetime = datetime(2023, 1, 1)
    __end: datetime = datetime(6000, 1, 1)

    def process(self, transactions) -> list:
        turnovers = {}

        for transaction in transactions:
            if not (self.__start <= transaction.period <= self.__end):
                continue

            key = (transaction.storage.id, transaction.nomenclature.id, transaction.range.id)

            if key not in turnovers:
                turnovers[key] = storage_turnover(transaction.storage, transaction.nomenclature, transaction.range)

            if transaction.type == transaction_type.INCOME:
                turnovers[key].turnover += transaction.quantity
            else:
                turnovers[key].turnover -= transaction.quantity

        return list(turnovers.values())
    
    @property
    def start(self) -> datetime:
        return self.__start

    @start.setter
    def start(self, value):
        CustomRaise.type_exception("start", value, datetime)
        self.__start = value

    @property
    def end(self) -> datetime:
        return self.__end

    @end.setter
    def end(self, value):
        CustomRaise.type_exception("end", value, datetime)
        self.__end = value
    
    def set_exception(self, e: Exception):
        self._inner_set_exception(e)