from src.file_manager import file_manager
from src.core.object_types import log_type
from src.core.object_types import log_levels
from src.settings_manager import settings_manager
from src.core.custom_raise import CustomRaise
from datetime import datetime
import os

class log_manager():
    __settings_manager: settings_manager = None
    __log_level: log_levels = log_levels.ERROR
    __folder_path: str = f"..{os.sep}data{os.sep}logs"
    __file_name: str = "logs.dat"

    def __init__(self, manager : settings_manager) -> None:
        super().__init__()
        CustomRaise.type_exception("settings_manager", manager, settings_manager)
        self.__settings_manager = manager
        if self.__settings_manager.settings.log_level is not None:
            self.__log_level = log_levels.set(manager.settings.log_level)
    
    def new(self, request: dict):
        level = log_type.ERROR
        message = "Incorrect request at log manager"
        if "status" in request:
            level = log_type.INFO
            message = request["status"]
        if "error" in request:
            message = request["error"]
        data = datetime.now().isoformat() + " - " + level.value + " - " + message
        if level in self.__log_level.value:
            return file_manager.file_append(self.__folder_path, self.__file_name, data)

    def new_debug(self, debug: str):
        if log_type.DEBUG in self.__log_level.value:
            data = datetime.now().isoformat() + " - DEBUG - " + debug
            return file_manager.file_append(self.__folder_path, self.__file_name, data)

    def new_debugs(self, debugs: list):
        if log_type.DEBUG in self.__log_level.value:
            for debug in debugs:
                data = datetime.now().isoformat() + " - DEBUG - " + debug
                return file_manager.file_append(self.__folder_path, self.__file_name, data)