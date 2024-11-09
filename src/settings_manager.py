from src.models.settings import settings
from src.core.abstract_logic import abstract_logic
from src.core.custom_raise import CustomRaise
from src.core.object_types import format_reporting
from src.logics.observe_service import observe_service
from src.core.object_types import event_type
from src.file_manager import file_manager
import json
import os

class settings_manager(abstract_logic):
    __instance = None
    __file_name = "settings (default).json"
    __settings:settings = settings()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(settings_manager, cls).__new__(cls, *args, **kwargs)
            cls.__instance.__init__()
        return cls.__instance

    def __init__(self) -> None:
        self.__settings = self.__default_settings()
        observe_service.append(self)

    def convert(self, data: dict):
        for key, value in data.items():
            if key == "report_format":
                formatted_value = format_reporting(value)
                setattr(self.__settings, key, formatted_value)
            elif hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    def open(self, file_name: str = "", file_path = os.curdir):
        CustomRaise.type_exception("file_name", file_name, str)
        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = self.__get_file_path(self.__file_name, file_path)
            
            if not full_name:
                self.__settings = self.__default_settings()
                CustomRaise.not_found_exception(self.__file_name)
            
            stream = open(full_name, encoding="utf-8")
            data = json.load(stream)
            self.convert(data)
            return True
        except Exception as e:
            self.__settings = self.__default_settings()
            self.set_exception(e)
            return False

    def save(self, folder_path: str = "../data/settings"):
        try:
            data = {
                "inn": self.__settings.inn,
                "account": self.__settings.account,
                "corr_account": self.__settings.correspondent_account,
                "bik": self.__settings.bik,
                "org_name": self.__settings.organization_name,
                "ownership_type": self.__settings.ownership_type,
                "report_format": self.__settings.report_format.value
            }
            return file_manager.json_write(folder_path, self.__file_name, data)
        except Exception as ex :
            self.set_exception(ex)
            return False

    @property
    def settings(self):
        return self.__settings

    def __default_settings(self):
        data = settings()
        data.inn = "700007000070"
        data.account = "70000700007"
        data.correspondent_account = "70000700007"
        data.bik = "123456789"
        data.organization_name = "Организация (default)"
        data.ownership_type = "частн"
        data.report_format = format_reporting.CSV
        return data
    
    @staticmethod
    def __get_file_path(filename:str = "", file_path = os.curdir):
        for root, _, _ in os.walk(file_path):
            full_name = os.path.join(root, filename)
            if os.path.isfile(full_name):
                return full_name
        return None
    
    def set_exception(self, e: Exception):
        self._inner_set_exception(e)
    
    def handle_event(self, type, params):
        super().handle_event(type, params)
        if type == event_type.CHANGE_DATEBLOCK:
            self.save()