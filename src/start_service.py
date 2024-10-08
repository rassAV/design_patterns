from src.core.abstract_logic import abstract_logic
from src.storage_reposity import storage_reposity
from src.models.range import range
from src.models.group_nomenclature import group_nomenclature
from src.models.nomenclature import nomenclature
from src.settings_manager import settings_manager
from src.models.settings import settings
from src.parsers_manager import parsers_manager
from src.core.custom_raise import CustomRaise

class start_service(abstract_logic):
    __reposity: storage_reposity = None
    __settings_manager: settings_manager = None

    def __init__(self, reposity : storage_reposity, manager: settings_manager) -> None:
        super().__init__()
        CustomRaise.type_exception("reposity", reposity, storage_reposity)
        self.__reposity = reposity
        self.__settings_manager = manager

    @property
    def settings(self) -> settings:
        return self.__settings_manager.settings
    
    @property
    def data(self):
        return self.__reposity.data
    
    def __create_unit_measurements(self):
        units = [
            range.default_gram(),
            range.default_kilogram(),
            range.default_ton()
        ]
        self.__reposity.data[storage_reposity.ranges_key()] = units
    
    def __create_nomenclature_group(self):
        list = [ group_nomenclature.default_group_source(), group_nomenclature.default_group_cold() ]
        self.__reposity.data[storage_reposity.groups_key()] = list
    
    def __create_nomenclature(self):
        nomenclatures = [
            nomenclature.default_nomenclature_1(),
            nomenclature.default_nomenclature_2()
        ]
        self.__reposity.data[storage_reposity.nomenclature_key()] = nomenclatures

    def __create_receipts(self):
        self.__reposity.data[storage_reposity.receipts_key()] = parsers_manager.parse_md_receipts()

    def create(self):
        self.__create_unit_measurements()
        self.__create_nomenclature_group()
        self.__create_nomenclature()
        self.__create_receipts()

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)