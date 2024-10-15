import unittest
from src.logics.prototype_manager import prototype_manager
from src.dto.filter import filter
from src.storage_reposity import storage_reposity
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.dto.filter_type import filter_type

class test_prototype(unittest.TestCase):
    def test_prototype_nomenclature_by_id(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.nomenclature_key() ]
        item = data[0]
        filt = filter(id=item.id)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) == 2
        assert result.data[0] == item

    def test_prototype_nomenclature_by_equals(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.nomenclature_key() ]
        item = data[0]
        filt = filter(name=item.name, type = filter_type.EQUALS)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) == 2
        assert result.data[0] == item

    def test_prototype_nomenclature_by_like(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.nomenclature_key() ]
        item = data[0]
        filt = filter(name=item.name, type=filter_type.LIKE)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) > 0
        assert result.data[0].name.startswith(item.name)

    def test_prototype_ranges_by_equals(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.ranges_key() ]
        item = data[0]
        filt = filter(name=item.name, type=filter_type.EQUALS)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) == 3
        assert result.data[0] == item

    def test_prototype_ranges_by_like(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.ranges_key() ]
        item = data[0]
        filt = filter(name=item.name, type=filter_type.LIKE)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) > 0
        assert result.data[0].name.startswith(item.name)

    def test_prototype_groups_by_equals(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.groups_key() ]
        item = data[0]
        filt = filter(name=item.name, type=filter_type.EQUALS)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_groups_by_like(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.groups_key() ]
        item = data[0]
        filt = filter(name=item.name, type=filter_type.LIKE)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) > 0
        assert result.data[0].name.startswith(item.name)

    def test_prototype_reciepts_by_equals(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.receipts_key() ]
        item = data[0]
        filt = filter(name=item.name, type=filter_type.EQUALS)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_reciepts_by_like(self):
        # Подготовка
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        data = reposity.data[ storage_reposity.receipts_key() ]
        item = data[0]
        filt = filter(name=item.name, type=filter_type.LIKE)
        prototype = prototype_manager(data)
        result = prototype.create(data, filt)

        # Проверка
        assert len(result.data) > 0
        assert result.data[0].name.startswith(item.name)