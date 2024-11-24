from src.file_manager import file_manager
from src.core.object_types import log_type
from src.settings_manager import settings_manager
from src.core.custom_raise import CustomRaise
from datetime import datetime
import os

class log_manager():
    __settings_manager: settings_manager = None
    __log_level: log_type = log_type.ERROR
    __folder_path: str = f"..{os.sep}data{os.sep}logs"
    __file_name: str = "logs.dat"

    def __init__(self, manager : settings_manager) -> None:
        super().__init__()
        CustomRaise.type_exception("settings_manager", manager, settings_manager)
        self.__settings_manager = manager
        if self.__settings_manager.settings.log_level is not None:
            self.__log_level = self.__settings_manager.settings.log_level
    
    def new(self, request: dict):
        level = request["log_level"]
        message = request["message"]
        data = datetime.now().isoformat() + " - " + level.value + " - " + message
        if self.__log_level == log_type.ERROR:
            if level == log_type.ERROR:
                file_manager.file_append(self.__folder_path, self.__file_name, data)
        elif self.__log_level == log_type.INFO:
            if level == log_type.ERROR or level == log_type.INFO:
                file_manager.file_append(self.__folder_path, self.__file_name, data)
        else:
            file_manager.file_append(self.__folder_path, self.__file_name, data)

    def new_debugs(self, debugs: list):
        for debug in debugs:
            data = datetime.now().isoformat() + " - DEBUG - " + debug
            file_manager.file_append(self.__folder_path, self.__file_name, data)