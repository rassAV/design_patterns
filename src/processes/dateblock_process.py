from src.core.abstract_logic import abstract_logic
from datetime import datetime
from src.core.custom_raise import CustomRaise
from src.processes.turnover_process import turnover_process
from src.file_manager import file_manager
import os

class dateblock_process(abstract_logic):
    __file_name: str = "blocked_turnovers.json"

    def process(self, transactions):
        turnovers_new = {}
        turnovers_old = {}
        turnover = turnover_process()
        file = file_manager()
        folder = "../data/turnovers"

        if os.path.exists(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)), self.__file_name)):
            data = file.json_read(folder, self.__file_name)
            turnover.start = datetime.fromisoformat(data['date'])
            for turnover in turnover.process(transactions):
                turnovers_new[turnover.storage.id + turnover.nomenclature.id + turnover.range.id] = turnover.turnover
            turnovers_old = data['turnovers']
            turnovers_result = self.merge_dicts(turnovers_old, turnovers_new)
        else:
            for turnover in turnover.process(transactions):
                turnovers_new[turnover.storage.id + turnover.nomenclature.id + turnover.range.id] = turnover.turnover
            turnovers_result = turnovers_new
        
        result = {
            "date": datetime.now().isoformat(), 
            "turnovers": turnovers_result
            }
        return file.json_write(folder, self.__file_name, result)
    
    def merge_dicts(d1, d2):
        result = d1.copy()
        for key, value in d2.items():
            if key in result:
                result[key] += value
            else:
                result[key] = value
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