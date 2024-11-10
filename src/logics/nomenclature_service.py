from src.core.abstract_logic import abstract_logic
from src.logics.observe_service import observe_service
from src.core.object_types import event_type
from src.dto.filter_type import filter_type
from src.dto.filter import filter
from src.logics.prototype_manager import prototype_manager
from src.storage_reposity import storage_reposity
from src.processes.dateblock_process import dateblock_process
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
        nomenclature = next(iter(self.get_data(filter(id=id, type=filter_type.EQUALS), storage_reposity.nomenclature_key())), None)
        if not nomenclature:
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
        return {"status": "Nomenclature successfully added"}

    def update_nomenclature(self, request):
        id = request.get('id')
        if not id:
            return {"error": "ID is required"}
        nomenclature = next(iter(self.get_data(filter(id=id, type=filter_type.EQUALS), storage_reposity.nomenclature_key())), None)
        if not nomenclature:
            return {"error": f"Nomenclature with ID {id} not found"}
        
        result = self.replace_nomenclature_data(nomenclature, request)
        if "error" in result:
            return result

        receipts = self.__reposity.data.get(storage_reposity.receipts_key(), [])
        for recipy in receipts:
            for ingredient in recipy.ingredients:
                if ingredient.nomenclature.id == id:
                    result = self.replace_nomenclature_data(ingredient.nomenclature, request)
                    if "error" in result:
                        return result
        
        transactions = self.__reposity.data.get(storage_reposity.transactions_key(), [])
        for transaction in transactions:
            if transaction.nomenclature.id == id:
                result = self.replace_nomenclature_data(transaction.nomenclature, request)
                if "error" in result:
                    return result

        dateblock = dateblock_process()
        dateblock.process(transactions)

        return {"status": "Nomenclature successfully updated"}

    def replace_nomenclature_data(self, nomenclature, request):
        if 'name' in request:
            nomenclature.name = request['name']
        if 'full_name' in request:
            nomenclature.full_name = request['full_name']
        if 'group_id' in request:
            group = next(iter(self.get_data(filter(id=request['group_id'], type=filter_type.EQUALS), storage_reposity.groups_key())), None)
            if not group:
                return {"error": f"Group with ID {request['group_id']} not found"}
            nomenclature.group = group
        if 'range_id' in request:
            rng = next(iter(self.get_data(filter(id=request['range_id'], type=filter_type.EQUALS), storage_reposity.ranges_key())), None)
            if not rng:
                return {"error": f"Range with ID {request['range_id']} not found"}
            nomenclature.range = rng
        return {"status": f"Successfully replaced"}

    def delete_nomenclature(self, request):
        id = request.get('id')
        if not id:
            return {"error": "ID is required"}
        filt = filter(id=id, type=filter_type.EQUALS)
        nomenclature = next(iter(self.get_data(filt, storage_reposity.nomenclature_key())), None)
        if not nomenclature:
            return {"error": f"Nomenclature with ID {id} not found"}
        receipts = next(iter(self.get_data(filt, storage_reposity.receipts_key())), None)
        if receipts:
            return {"error": f"Nomenclature can't deleted, because nomenclature used in receipts"}
        transactions = next(iter(self.get_data(filt, storage_reposity.transactions_key())), None)
        if transactions:
            return {"error": f"Nomenclature can't deleted, because nomenclature used in transactions"}
        self.__reposity.data[storage_reposity.nomenclature_key()] = [ n for n in self.__reposity.data[storage_reposity.nomenclature_key()] if n.id != id ]
        return {"status": "Nomenclature successfully deleted"}

    def set_exception(self, ex: Exception):
        super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
        if type == event_type.UPDATE_NOMENCLATURE:
            return self.update_nomenclature(params)
        elif type == event_type.DELETE_NOMENCLATURE:
            return self.delete_nomenclature(params)
        CustomRaise.operation_exception("Ошибка! В nomenclature_service.handle_event передан некорректный тип события!")