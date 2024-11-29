from enum import Enum

class format_reporting(Enum):
    CSV = ".csv"
    MD = ".md"
    JSON = ".json"
    XML = ".xml"
    DOCX = ".docx"
    XLSX = ".xlsx"

class transaction_type(Enum):
    INCOME = "Приход"
    OUTCOME = "Расход"

class event_type(Enum):
    FORMATS = "formats"
    GET_REPORT = "get_report"
    FILTER_DATA = "filter_data"
    TRANSACTIONS = "transactions"
    TURNOVER = "turnover"
    DATEBLOCK = "dateblock"
    GET_DATEBLOCK = "get_dateblock"
    GET_NOMENCLATURE = "get_nomenclature"
    ADD_NOMENCLATURE = "add_nomenclature"
    UPDATE_NOMENCLATURE = "update_nomenclature"
    DELETE_NOMENCLATURE = "delete_nomenclature"
    GET_BALANCE_LIST = "get_balance_list"
    SAVE_DATA = "save_data"
    LOAD_DATA = "load_data"

class log_type(Enum):
    ERROR = "ERROR"
    INFO = "INFO"
    DEBUG = "DEBUG"

class log_levels(Enum):
    ERROR = [log_type.ERROR]
    INFO = [log_type.ERROR, log_type.INFO]
    DEBUG = [log_type.ERROR, log_type.INFO, log_type.DEBUG]

    @classmethod
    def set(cls, level: log_type):
        if level == log_type.ERROR:
            return cls.ERROR
        elif level == log_type.INFO:
            return cls.INFO
        elif level == log_type.DEBUG:
            return cls.DEBUG