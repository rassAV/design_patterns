from src.logics.nomenclature_service import nomenclature_service
from src.logics.observe_service import observe_service
from src.core.object_types import event_type
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.storage_reposity import storage_reposity

import unittest

class test_observer(unittest.TestCase):
    def test_observe_service_get(self):
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        nmcl_service = nomenclature_service(reposity)

        nomenclature = start.data["nomenclature"]

        request = {}
        result = nmcl_service.get_nomenclature(request)
        assert result == {"error": "ID is required"}

        request = {"id": "incorrect"}
        result = nmcl_service.get_nomenclature(request)
        assert result == {"error": f"Nomenclature with ID incorrect not found"}

        request = {"id": nomenclature[0].id}
        result = nmcl_service.get_nomenclature(request)
        assert result == nomenclature[0]
    
    def test_observe_service_add(self):
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        nmcl_service = nomenclature_service(reposity)

        nomenclature = start.data["nomenclature"]
        groups = start.data["groups"]
        ranges = start.data["ranges"]

        request = {"name": "Test", "full_name": "Test Full", "group_id": "invalid_group", "range_id": "invalid_range"}
        result = nmcl_service.add_nomenclature(request)
        assert result == {"error": "Group with ID invalid_group not found"}

        request = {"name": "Test", "full_name": "Test Full", "group_id": groups[0].id, "range_id": "invalid_range"}
        result = nmcl_service.add_nomenclature(request)
        assert result == {"error": "Range with ID invalid_range not found"}

        request = {"name": "Test", "full_name": "Test Full", "group_id": groups[0].id, "range_id": ranges[0].id}
        result = nmcl_service.add_nomenclature(request)
        assert result == {"status": "Nomenclature successfully added"}
        assert nomenclature[-1].full_name == "Test Full"
    
    def test_observe_service_update(self):
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        nmcl_service = nomenclature_service(reposity)

        nomenclature = start.data["nomenclature"]
        groups = start.data["groups"]
        ranges = start.data["ranges"]

        request = {}
        result = observe_service.raise_event(event_type.UPDATE_NOMENCLATURE, request)
        assert result["nomenclature_service"] == {"error": "ID is required"}

        request = {"id": "incorrect"}
        result = observe_service.raise_event(event_type.UPDATE_NOMENCLATURE, request)
        assert result["nomenclature_service"] == {"error": f"Nomenclature with ID incorrect not found"}

        request = {"id": nomenclature[0].id, "name": "Test", "full_name": "Test Full", "group_id": "invalid_group", "range_id": "invalid_range"}
        result = observe_service.raise_event(event_type.UPDATE_NOMENCLATURE, request)
        assert result["nomenclature_service"] == {"error": "Group with ID invalid_group not found"}

        request = {"id": nomenclature[0].id, "name": "Test", "full_name": "Test Full", "group_id": groups[0].id, "range_id": "invalid_range"}
        result = observe_service.raise_event(event_type.UPDATE_NOMENCLATURE, request)
        assert result["nomenclature_service"] == {"error": "Range with ID invalid_range not found"}

        request = {"id": nomenclature[0].id, "name": "Test", "full_name": "Test Full", "group_id": groups[0].id, "range_id": ranges[0].id}
        result = observe_service.raise_event(event_type.UPDATE_NOMENCLATURE, request)
        assert result["nomenclature_service"] == {"status": "Nomenclature successfully updated"}
    
    def test_observe_service_delete(self):
        manager = settings_manager()
        manager.open("settings1.json", "../")
        reposity = storage_reposity()
        start = start_service(reposity, manager)
        start.create()
        nmcl_service = nomenclature_service(reposity)

        nomenclature = start.data["nomenclature"]
        groups = start.data["groups"]
        ranges = start.data["ranges"]
        transactions = start.data["transactions"]
        transactions[0].nomenclature = nomenclature[0]

        request = {}
        result = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, request)
        assert result["nomenclature_service"] == {"error": "ID is required"}

        request = {"id": "incorrect"}
        result = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, request)
        assert result["nomenclature_service"] == {"error": f"Nomenclature with ID incorrect not found"}

        request = {"id": nomenclature[0].id}
        result = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, request)
        assert result["nomenclature_service"] == {"error": f"Nomenclature can't deleted, because nomenclature used in transactions"}, f"{result}"

        assert len(nomenclature) == 2
        request = {"name": "Test", "full_name": "Test Full", "group_id": groups[0].id, "range_id": ranges[0].id}
        result = nmcl_service.add_nomenclature(request)
        assert len(nomenclature) == 3

        request = {"id": nomenclature[-1].id}
        result = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, request)
        nomenclature = start.data["nomenclature"]
        assert result["nomenclature_service"] == {"status": "Nomenclature successfully deleted"}
        assert len(nomenclature) == 2