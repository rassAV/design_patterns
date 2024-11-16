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
    UPDATE_NOMENCLATURE = "upd_nmcl"
    DELETE_NOMENCLATURE = "del_nmcl"