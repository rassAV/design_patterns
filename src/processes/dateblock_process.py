from src.models.storage_turnover import storage_turnover
from src.core.abstract_logic import abstract_logic
from src.core.object_types import transaction_type
from datetime import datetime
from src.core.custom_raise import CustomRaise
from src.processes.turnover_process import turnover_process
import os
import json

class dateblock_process(abstract_logic):
    __file_name: str = "blocked_turnovers.json"

    def process(self, transactions):
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/turnovers"))
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        full_path = os.path.join(full_path, self.__file_name)

        turnovers_new = {}
        turnovers_old = {}

        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            turnover = turnover_process()
            turnover.start = datetime.fromisoformat(data['date'])
            for turnover in turnover.process(transactions):
                turnovers_new[turnover.storage.id + turnover.nomenclature.id + turnover.range.id] = turnover.turnover
            turnovers_old = data['turnovers']
            result = {"date":datetime.now().isoformat(), "turnovers":self.merge_dicts(turnovers_old, turnovers_new)}
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(json.dumps(result, ensure_ascii=False, indent=4))
        except:
            try:
                turnover = turnover_process()
                for turnover in turnover.process(transactions):
                    turnovers_new[turnover.storage.id + turnover.nomenclature.id + turnover.range.id] = turnover.turnover
                result = {
                    "date": datetime.now().isoformat(), 
                    "turnovers": turnovers_new
                    }
                with open(full_path, 'w', encoding='utf-8') as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
            except:
                return False
        return True
    
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