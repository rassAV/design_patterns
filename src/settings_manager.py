from src.models.settings import settings
from src.core.abstract_logic import abstract_logic
from src.core.custom_raise import CustomRaise

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

    def convert(self, data: dict):
        for key, value in data.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    def open(self, file_name:str = "", file_path = os.curdir):
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

    @property
    def settings(self):
        return self.__settings

    def __default_settings(self):
        data = settings()
        data.inn = "700007000070"
        data.account = "70000700007"
        data.corr_account = "70000700007"
        data.bik = "123456789"
        data.organization_name = "Организация (default)"
        data.ownership_type = "частн"
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