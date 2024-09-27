from src.core.custom_raise import CustomRaise
from src.core.format_reporting import format_reporting

class settings:
    __inn = ""
    __account = ""
    __correspondent_account = ""
    __bik = ""
    __organization_name = ""
    __ownership_type = ""
    __report_format: format_reporting = None

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value:str):
        CustomRaise.type_exception("inn", value, str)
        CustomRaise.length_required_exception("inn", value, 12)
        self.__inn = value
    
    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value:str):
        CustomRaise.type_exception("account", value, str)
        CustomRaise.length_required_exception("account", value, 11)
        self.__account = value
    
    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value:str):
        CustomRaise.type_exception("correspondent_account", value, str)
        CustomRaise.length_required_exception("correspondent_account", value, 11)
        self.__correspondent_account = value
    
    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value:str):
        CustomRaise.type_exception("bik", value, str)
        CustomRaise.length_required_exception("bik", value, 9)
        self.__bik = value
    
    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value:str):
        CustomRaise.type_exception("organization_name", value, str)
        self.__organization_name = value

    @property
    def ownership_type(self):
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value:str):
        CustomRaise.type_exception("ownership_type", value, str)
        CustomRaise.length_required_exception("ownership_type", value, 5)
        self.__ownership_type = value

    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value: format_reporting):
        CustomRaise.type_exception("report_format", value, format_reporting)
        self.__report_format = value