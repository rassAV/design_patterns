from src.core.abstract_logic import abstract_logic
from src.logics.observe_service import observe_service
from src.core.object_types import event_type
from src.dto.filter_type import filter_type
from src.dto.filter import filter
from src.logics.prototype_manager import prototype_manager
from src.storage_reposity import storage_reposity
from src.file_manager import file_manager
from src.core.custom_raise import CustomRaise

class nomenclature_service(abstract_logic):
    def __init__(self, reposity: storage_reposity):
        observe_service.append(self)
        self.__reposity = reposity

    def get_data(self, filt: filter, key: str):
        data = self.__reposity.data.get(key, [])
        prototype = prototype_manager(data)
        return prototype.create(data, filt).data

    def get_nomenclature(self, request):
        id = request.get('id')
        if not id:
            return {"error": "ID is required"}
        nomenclature = self.get_data(filter(id=id, type=filter_type.EQUALS), storage_reposity.nomenclature_key())
        if len(nomenclature) == 0:
            return {"error": f"Nomenclature with ID {id} not found"}
        return nomenclature

    def add_nomenclature(self, request):
        name = request.get('name')
        full_name = request.get('full_name')
        group_id = request.get('group_id')
        range_id = request.get('range_id')

        group_filt = filter(id=group_id, type=filter_type.EQUALS)
        group = next(iter(self.get_data(group_filt, storage_reposity.groups_key())), None)
        if not group:
            return {"error": f"Group with ID {group_id} not found"}

        rng_filt = filter(id=range_id, type=filter_type.EQUALS)
        rng = next(iter(self.get_data(rng_filt, storage_reposity.ranges_key())), None)
        if not rng:
            return {"error": f"Range with ID {range_id} not found"}

        nomenclature = nomenclature(full_name, group, rng)
        nomenclature.name = name
        if self.get_data(filter(id=nomenclature.id, type=filter_type.EQUALS), storage_reposity.nomenclature_key()):
            return {"error": f"Nomenclature with ID {nomenclature.id} already exists"}

        self.__reposity.data[storage_reposity.nomenclature_key()].append(nomenclature)
        return nomenclature

    def set_exception(self, ex: Exception):
        super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)