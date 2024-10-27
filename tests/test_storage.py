from src.settings_manager import settings_manager
from src.start_service import start_service
from src.storage_reposity import storage_reposity
from src.models.storage_transaction import storage_transaction
from src.processes.turnover_process import turnover_process
from src.core.object_types import transaction_type
from datetime import datetime

import unittest

class test_storage(unittest.TestCase):
    def test_storage_turnover(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        transactions = start.data["transactions"]
        transactions.append(storage_transaction.default_transaction_1())

        storage = transactions[0].storage
        nomenclature = transactions[0].nomenclature
        range = transactions[0].range

        transactions[1].storage = storage
        transactions[1].nomenclature = nomenclature
        transactions[1].range = range
        transactions[3].storage = storage
        transactions[3].nomenclature = nomenclature
        transactions[3].range = range
        transactions[3].quantity = 150
        transactions[3].type = transaction_type.INCOME
        
        turnover = turnover_process()
        result = turnover.process(transactions)

        # Проверка
        assert result[0].turnover == -200, f"Неверное значение result[0].turnover = {result[0].turnover}, ожидалось значение -200"

    def test_storage_turnover_in_period(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        transactions = start.data["transactions"]
        transactions.append(storage_transaction.default_transaction_1())

        storage = transactions[0].storage
        nomenclature = transactions[0].nomenclature
        range = transactions[0].range

        transactions[0].period = datetime(2024, 3, 25)
        transactions[1].storage = storage
        transactions[1].nomenclature = nomenclature
        transactions[1].range = range
        transactions[1].period = datetime(2024, 7, 12)
        transactions[3].storage = storage
        transactions[3].nomenclature = nomenclature
        transactions[3].range = range
        transactions[3].period = datetime(2030, 10, 5)
        transactions[3].quantity = 150
        transactions[3].type = transaction_type.INCOME
        
        turnover = turnover_process()
        turnover.start = datetime(2024, 1, 1)
        turnover.end = datetime(2025, 1, 1)
        result = turnover.process(transactions)

        # Проверка
        assert result[0].turnover == -350, f"Неверное значение result[0].turnover = {result[0].turnover}, ожидалось значение -350"