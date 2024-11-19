from src.models.storage_turnover import storage_turnover
from src.core.abstract_logic import abstract_logic
from src.core.object_types import transaction_type
from datetime import datetime
from src.core.custom_raise import CustomRaise

class turnover_process(abstract_logic):
    __start: datetime = datetime(1, 1, 1)
    __end: datetime = datetime(6000, 1, 1)

    def process(self, transactions, extra_data = False):
        turnovers = {}
        incomes = {}
        outcomes = {}

        for transaction in transactions:
            if not (self.__start <= transaction.period <= self.__end):
                continue

            key = transaction.storage.id + transaction.nomenclature.id + transaction.range.id

            if key not in turnovers:
                turnovers[key] = storage_turnover(transaction.storage, transaction.nomenclature, transaction.range)
            if key not in incomes:
                incomes[key] = 0.0
            if key not in outcomes:
                outcomes[key] = 0.0

            if transaction.type == transaction_type.INCOME:
                incomes[key] += transaction.quantity
                turnovers[key].turnover += transaction.quantity
            else:
                outcomes[key] += transaction.quantity
                turnovers[key].turnover -= transaction.quantity

        if extra_data:
            return incomes, outcomes, list(turnovers.values())
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
    
    def handle_event(self, type, params):
        super().handle_event(type, params)