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
    DELETE_NOMENCLATURE = "del_nmcl"
    CHANGE_NOMENCLATURE = "chg_nmcl"
    CHANGE_RANGE = "chg_rng"
    CHANGE_DATEBLOCK = "chg_dtbl"