from src.settings_manager import settings_manager
from src.start_service import start_service
from src.storage_reposity import storage_reposity
from src.models.storage_transaction import storage_transaction
from src.processes.turnover_process import turnover_process
from src.processes.dateblock_process import dateblock_process
from src.core.object_types import transaction_type
from datetime import datetime
import os
import json
import time

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

    def test_storage_dateblock(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        transactions = start.data["transactions"]

        storage = transactions[0].storage
        nomenclature = transactions[0].nomenclature
        range = transactions[0].range

        transactions[0].period = datetime(2024, 3, 25)
        transactions[1].storage = storage
        transactions[1].nomenclature = nomenclature
        transactions[1].range = range
        transactions[1].period = datetime(2024, 7, 12)
        
        dateblock = dateblock_process()
        dateblock.file_name = "test_blocked_turnovers.json"
        result = dateblock.process(transactions)

        # Проверка
        assert result
        file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/turnovers")), "test_blocked_turnovers.json")
        assert os.path.exists(file_path), "Файл не был создан."
        with open(file_path, 'r', encoding='utf-8') as file:
            data = list(json.load(file)["turnovers"].values())
            assert len(data) == 2
            assert (data[0] == 1.25 and data[1] == -350) or (data[0] == -350 and data[1] == 1.25)

        # Подготовка
        transactions.append(storage_transaction.default_transaction_1())
        transactions[3].storage = storage
        transactions[3].nomenclature = nomenclature
        transactions[3].range = range
        transactions[3].period = datetime.now()
        transactions[3].quantity = 150
        transactions[3].type = transaction_type.INCOME

        result = dateblock.process(transactions)

        # Проверка
        assert result
        file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/turnovers")), "test_blocked_turnovers.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = list(json.load(file)["turnovers"].values())
            assert len(data) == 2
            assert (data[0] == 1.25 and data[1] == -200) or (data[0] == -200 and data[1] == 1.25)

    def test_storage_load_dateblock(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        transactions = start.data["transactions"]

        storage = transactions[0].storage
        nomenclature = transactions[0].nomenclature
        rng = transactions[0].range

        for i in range(15000):
            transactions.append(storage_transaction.default_transaction_1())
            transactions[-1].storage = storage
            transactions[-1].nomenclature = nomenclature
            transactions[-1].range = rng
            transactions[-1].quantity = 150
            transactions[-1].type = transaction_type.INCOME
        
        dateblock = dateblock_process()
        dateblock.file_name = "test_blocked_turnovers_load.json"
        dateblock.process(transactions)

        for i in range(15000):
            transactions.append(storage_transaction.default_transaction_1())
            transactions[-1].storage = storage
            transactions[-1].nomenclature = nomenclature
            transactions[-1].range = rng
            transactions[-1].period = datetime.now()
            transactions[-1].quantity = 125
            transactions[-1].type = transaction_type.OUTCOME

        start_time = time.time()
        dateblock.process(transactions)
        time_with_dateblock = time.time() - start_time

        for i in range(15000):
            transactions.append(storage_transaction.default_transaction_1())
            transactions[-1].storage = storage
            transactions[-1].nomenclature = nomenclature
            transactions[-1].range = rng
            transactions[-1].quantity = 150
            transactions[-1].type = transaction_type.INCOME
            transactions.append(storage_transaction.default_transaction_1())
            transactions[-1].storage = storage
            transactions[-1].nomenclature = nomenclature
            transactions[-1].range = rng
            transactions[-1].quantity = 125
            transactions[-1].type = transaction_type.OUTCOME

        dateblock.file_name = "test_blocked_turnovers_load_2.json"
        start_time = time.time()
        dateblock.process(transactions)
        time_without_dateblock = time.time() - start_time

        with open("tests/test_storage_load_dateblock_results.md", "w", encoding="utf-8") as file:
            file.write("# Результаты измерения времени выполнения\n\n")
            file.write(f"### Время выполнения с блокировкой дат: {time_with_dateblock:.6f} секунд\n\n")
            file.write(f"### Время выполнения без блокировки дат: {time_without_dateblock:.6f} секунд\n\n")