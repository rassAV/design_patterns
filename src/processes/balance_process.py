from src.core.abstract_logic import abstract_logic
from datetime import datetime
from src.processes.turnover_process import turnover_process
from src.file_manager import file_manager
from src.core.custom_raise import CustomRaise

class balance_process(abstract_logic):
    __file_name: str = "balance_list.json"

    def process(self, transactions, d1, d2):
        data1 = datetime.strptime(d1, "%Y-%m-%d")
        data2 = datetime.strptime(d2, "%Y-%m-%d")

        turnovers1= {}
        incomes = {}
        outcomes = {}
        turnovers2 = {}
        turnover = turnover_process()
        turnover.end = data1

        for t in turnover.process(transactions):
            turnovers1[t.storage.id + t.nomenclature.id + t.range.id] = t.turnover
        turnover.start = data1
        turnover.end = data2
        incomes, outcomes, turnovers = turnover.process(transactions, True)
        for t in turnovers:
            turnovers2[t.storage.id + t.nomenclature.id + t.range.id] = t.turnover
        
        result = {
            "date1": data1.isoformat(),
            "date2": data2.isoformat(),
            "turnovers1": turnovers1,
            "incomes": incomes,
            "outcomes": outcomes,
            "turnovers2": turnovers2,
            }
        return result
    
    def save(self, transactions, d1, d2):
        file = file_manager()
        folder = "../data/balances"
        result = self.process(transactions, d1, d2)
        return file.json_write(folder, self.__file_name, result)
    
    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        CustomRaise.type_exception("file_name", value, str)
        self.__file_name = value
    
    def set_exception(self, e: Exception):
        self._inner_set_exception(e)

    def handle_event(self, type, logs, params):
        super().handle_event(type, logs, params)