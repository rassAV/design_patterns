from src.core.abstract_logic import abstract_logic
from datetime import datetime
from src.processes.turnover_process import turnover_process
from src.file_manager import file_manager
from src.core.custom_raise import CustomRaise

class balance_process(abstract_logic):
    __file_name: str = "balance_list.json"

    def process(self, transactions, data1, data2):
        turnovers1= {}
        incomes = {}
        outcomes = {}
        turnovers2 = {}
        turnover = turnover_process()
        turnover.end = datetime(data1)
        file = file_manager()
        folder = "../data/balances"

        for turnover in turnover.process(transactions):
            turnovers1[turnover.storage.id + turnover.nomenclature.id + turnover.range.id] = turnover.turnover
        turnover.start = datetime(data1)
        turnover.end = datetime(data2)
        incomes, outcomes, turnovers = turnover.process(transactions, True)
        for turnover in turnovers:
            turnovers2[turnover.storage.id + turnover.nomenclature.id + turnover.range.id] = turnovers.turnover
        
        result = {
            "date1": datetime(data1).isoformat(),
            "date2": datetime(data2).isoformat(),
            "turnovers1": turnovers1,
            "incomes": incomes,
            "outcomes": outcomes,
            "turnovers2": turnovers2,
            }
        file.json_write(folder, self.__file_name, result)
        return result
    
    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        CustomRaise.type_exception("file_name", value, str)
        self.__file_name = value
    
    def set_exception(self, e: Exception):
        self._inner_set_exception(e)

    def handle_event(self, type, params):
        super().handle_event(type, params)