from abc import ABC, abstractmethod
from src.core.object_types import event_type
from src.core.custom_raise import CustomRaise

class abstract_logic(ABC):
    __error_text: str = ""

    @property
    def error_text(self) -> str:
        return self.__error_text.strip()
    
    @error_text.setter
    def error_text(self, message: str):
        self.__error_text = message.strip()
    
    @property
    def is_error(self) -> bool:
        return self.error_text != ""

    def _inner_set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"

    @abstractmethod
    def set_exception(self, ex: Exception):
        pass

    @abstractmethod
    def handle_event(self, type: event_type, params):
        CustomRaise.type_exception("event_type", type, event_type)