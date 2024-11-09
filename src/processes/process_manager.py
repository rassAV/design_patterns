from src.core.abstract_logic import abstract_logic
from src.core.custom_raise import CustomRaise

class process_manager(abstract_logic):
    def __init__(self):
        self.__processes = {}     

    def register(self, name: str, process_class):
        self.__processes[name] = process_class

    def get(self, name: str):
        process_class = self.__processes.get(name)
        if not process_class:
            CustomRaise.operation_exception(f"Процесс с именем {name} не найден!")
        return process_class()
    
    def set_exception(self, e: Exception):
        self._inner_set_exception(e)

    def handle_event(self, type, params):
        super().handle_event(type, params)