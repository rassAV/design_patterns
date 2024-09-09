import json
import os
from settings import settings

class settings_manager:
    __file_name = "settings (default).json"
    __settings:settings = settings()

    # def __new__(cls):
    #     if not hasattr(cls, "instance"):
    #         cls.instance = super(settings_manager, cls).__new__(cls)
    #     return cls.instance

    def __init__(self) -> None:
        self.__settings = self.__default_settings()

    def convert(self, data: dict):
        for key, value in data.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    def open(self, file_name:str = ""):
        if not isinstance(file_name, str):
            raise TypeError("~ Некорректно передан параметр!")

        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = self.__get_file_path(self.__file_name)
            if not full_name:
                self.__settings = self.__default_setting()
                raise TypeError(f"~ Файл {self.__file_name} не найден!\nУстановлены настройки по умолчанию!")
            
            stream = open(full_name, encoding="utf-8")
            data = json.load(stream)
            self.convert(data)

            print(f"~ Файл {self.__file_name} успешно загружен.")
            return True
        except:
            self.__settings = self.__default_settings()
            print(f"~ Ошибка загрузки файла {self.__file_name}!\nУстановлены настройки по умолчанию!")
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
    def __get_file_path(filename, file_path = os.curdir):
        for root, _, _ in os.walk(file_path):
            full_name = os.path.join(root, filename)
            if os.path.isfile(full_name):
                return full_name
        return None