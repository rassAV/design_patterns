import json
import os

class settings:
    __inn = ""
    __account = ""
    __correspondent_account = ""
    __bik = ""
    __organization_name = ""
    __ownership_type = ""

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value:str):
        if not isinstance(value, str):
            raise TypeError("~ Некорректно передан параметр!")
        if not value.isdigit() or len(value) != 12:
            raise TypeError("~ ИНН должен состоять из 12 цифр!")
        self.__inn = value
    
    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value:str):
        if not isinstance(value, str):
            raise TypeError("~ Некорректно передан параметр!")
        if not value.isdigit() or len(value) != 11:
            raise TypeError("~ Счет  должен состоять из 11 цифр!")
        self.__account = value
    
    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value:str):
        if not isinstance(value, str):
            raise TypeError("~ Некорректно передан параметр!")
        if not value.isdigit() or len(value) != 11:
            raise TypeError("~ Корреспондентский счет должен состоять из 11 цифр!")
        self.__correspondent_account = value
    
    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value:str):
        if not isinstance(value, str):
            raise TypeError("~ Некорректно передан параметр!")
        if not value.isdigit() or len(value) != 9:
            raise TypeError("~ БИК должен состоять из 9 цифр!")
        self.__bik = value
    
    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value:str):
        if not isinstance(value, str):
            raise TypeError("~ Некорректно передан параметр!")
        self.__organization_name = value

    @property
    def ownership_type(self):
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value:str):
        if not isinstance(value, str):
            raise TypeError("~ Некорректно передан параметр!")
        if len(value) != 5:
            raise TypeError("~ Вид собственности должен состоять из 5 символов!")
        self.__ownership_type = value

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

manager1 = settings_manager()
manager1.open("settings1.json")
print(f"settings1: {manager1.settings.inn}")

manager2 = settings_manager()
manager2.open("settings2.json")
print(f"settings2: {manager2.settings.inn}")