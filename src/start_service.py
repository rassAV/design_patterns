from src.core.abstract_logic import abstract_logic
from src.storage_reposity import storage_reposity
from src.models.range import range
from src.models.group_nomenclature import group_nomenclature
from src.models.nomenclature import nomenclature
from src.settings_manager import settings_manager
from src.models.settings import settings
from src.parsers_manager import parsers_manager
from src.core.custom_raise import CustomRaise
from src.models.storage import storage
from src.models.storage_transaction import storage_transaction
from src.reports.json_report import json_report

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

    def __create_storages(self):
        storages = [
            storage.default_storage_1(),
            storage.default_storage_2()
        ]
        self.__reposity.data[storage_reposity.storages_key()] = storages

    def __create_transactions(self):
        transactions = [
            storage_transaction.default_transaction_1(),
            storage_transaction.default_transaction_2(),
            storage_transaction.default_transaction_3()
        ]
        self.__reposity.data[storage_reposity.transactions_key()] = transactions

    def __create_default_data(self):
        self.__create_unit_measurements()
        self.__create_nomenclature_group()
        self.__create_nomenclature()
        self.__create_receipts()
        self.__create_storages()
        self.__create_transactions()

    def create(self):
        if not self.settings.first_start:
            result = self.load()
            if result:
                self.__create_default_data()
        else:
            self.__create_default_data

    def save(self):
        report = json_report()
        report.create(self.data[self.data.keys()])
        return report.save("../../data/reposities", f"reposity_{self.__settings_manager.__file_name[7:]}")

    def load(self):
        try:
            if self.settings.first_start:
                return False
            report = json_report()
            result = report.load("../../data/reposities", f"reposity_{self.__settings_manager.__file_name[7:]}")
            if "error" in result:
                return False
            self.data = result
            return True
        except:
            return False

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
    
    def handle_event(self, type, params):
        super().handle_event(type, params)