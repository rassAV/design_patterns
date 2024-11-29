from src.core.abstract_logic import abstract_logic

class storage_reposity(abstract_logic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(storage_reposity, cls).__new__(cls)
        return cls.instance 

    @property
    def data(self):
        return self.__data

    @staticmethod
    def ranges_key() -> str:
        return "ranges"
    
    @staticmethod
    def groups_key() -> str:
        return "groups"

    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature"
    
    @staticmethod
    def receipts_key() -> str:
        return "receipts"
    
    @staticmethod
    def storages_key() -> str:
        return "storages"

    @staticmethod
    def transactions_key() -> str:
        return "transactions"
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type, logs, params):
        super().handle_event(type, logs, params)