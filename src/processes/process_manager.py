from src.core.custom_raise import CustomRaise

class process_manager:
    def __init__(self):
        self.__processes = {}

    def register(self, name: str, process_class):
        self.__processes[name] = process_class

    def get(self, name: str):
        process_class = self.__processes.get(name)
        if not process_class:
            CustomRaise.operation_exception(f"Процесс с именем {name} не найден!")
        return process_class()