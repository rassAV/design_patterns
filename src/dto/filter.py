from src.dto.filter_type import filter_type
from src.core.custom_raise import CustomRaise
from src.core.abstract_logic import abstract_logic

class filter(abstract_logic):
    def __init__(self, name: str = "", id: str = "", type: filter_type = filter_type.EQUALS):
        self.__name: str = name
        self.__id: str = id
        self.__type: filter_type = type

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        CustomRaise.non_empty_exception("name", value)
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, value: str):
        CustomRaise.non_empty_exception("id", value)
        self.__id = value

    @property
    def type(self) -> filter_type:
        return self.__type
    
    @type.setter
    def type(self, value: filter_type):
        CustomRaise.type_exception("filter_type", value, filter_type)
        self.__type = value

    @staticmethod
    def from_dict(data):
        name = data.get('name', "")
        id = data.get('id', "")
        type_value = int(data.get('type', filter_type.EQUALS.value))
        type_enum = filter_type(type_value)
        
        CustomRaise.type_exception("filter_type", type_enum, filter_type)
        return filter(name=name, id=id, type=type_enum)
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type, logs, params):
        super().handle_event(type, logs, params)