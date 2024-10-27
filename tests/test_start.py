from src.settings_manager import settings_manager
from src.start_service import start_service
from src.storage_reposity import storage_reposity
from datetime import datetime
from src.core.object_types import transaction_type

import unittest

class test_start(unittest.TestCase):
    def test_create_start_service(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)

        # Проверки
        assert start is not None

    def test_create_ranges(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        # Проверки
        assert len(start.data["ranges"]) > 0
        assert start.data["ranges"][2].unit_range == "тонна"
        assert start.data["ranges"][2].conversion_factor == 1000
        assert start.data["ranges"][2].base_range.unit_range == "килограмм"
        assert start.data["ranges"][2].base_range.conversion_factor == 1000

    def test_create_nomenclature_groups(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        # Проверки
        assert len(start.data["groups"]) > 0
        assert start.data["groups"][0].name == "Сырьё"
        assert start.data["groups"][1].name == "Заморозка"

    def test_create_nomenclature(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        # Проверки
        assert len(start.data["nomenclature"]) > 0
        assert start.data["nomenclature"][0].full_name == "Мука"
        assert start.data["nomenclature"][0].group.name == "Сырьё"
        assert start.data["nomenclature"][0].range.unit_range == "килограмм"
        assert start.data["nomenclature"][0].range.conversion_factor == 1000

    def test_create_receipts(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        # Проверки
        assert len(start.data["receipts"]) > 0
        assert start.data["receipts"][0].name == "ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ"
        assert start.data["receipts"][0].servings == "`10 порций`"
        assert start.data["receipts"][0].ingredients[0].name == "Пшеничная мука"
        assert start.data["receipts"][0].ingredients[0].unit_value == 100
        assert start.data["receipts"][0].ingredients[0].range.unit_range == "гр"
        assert start.data["receipts"][0].ingredients[0].nomenclature.group.name == "Сырьё"
        assert start.data["receipts"][0].time == "`20 мин`"
        assert start.data["receipts"][0].instructions[0] == "1. Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см."
        assert start.data["receipts"][0].instructions[1] == "2. Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке."

    def test_create_storages(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        # Проверки
        assert len(start.data["storages"]) > 0
        assert start.data["storages"][0].name == "Default Storage 1"
        assert start.data["storages"][0].adress == "Россия, г. Ангарск, кв-л. 71, 4"

    def test_create_transactions(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()

        # Проверки
        assert len(start.data["transactions"]) > 0
        assert start.data["transactions"][0].storage.name == "Default Storage 1"
        assert start.data["transactions"][0].nomenclature.full_name == "Мука"
        assert start.data["transactions"][0].range.unit_range == "грамм"
        assert start.data["transactions"][0].quantity == 200.0
        assert isinstance(start.data["transactions"][0].period, datetime)
        assert start.data["transactions"][0].type == transaction_type.OUTCOME