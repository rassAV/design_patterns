from src.core.custom_raise import CustomRaise
from src.storage_reposity import storage_reposity
from src.models.storage import storage
from src.models.storage_transaction import storage_transaction
from src.models.recipe import recipe
from src.models.range import range
from src.models.nomenclature import nomenclature
from src.models.group_nomenclature import group_nomenclature
from datetime import datetime
from src.core.object_types import log_type
import os
import json

class file_manager():
    @staticmethod
    def json_read(folder_path, file_name):
        try:
            full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), folder_path))
            if not os.path.exists(full_path):
                os.makedirs(full_path)

            full_path = os.path.join(full_path, file_name)
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                mapping = {
                    storage_reposity.ranges_key(): range,
                    storage_reposity.groups_key(): group_nomenclature,
                    storage_reposity.nomenclature_key(): nomenclature,
                    storage_reposity.receipts_key(): recipe,
                    storage_reposity.storages_key(): storage,
                    storage_reposity.transactions_key(): storage_transaction
                }

                for key, value in data.items():
                    model_class = mapping.get(key)
                    if model_class:
                        data[key] = [model_class.from_json(item) for item in value]
                
                return data
            else:
                return {"error": f"json file {file_name} not found"}
        except Exception as e:
            return {"error": f"can not read json file {file_name}: {str(e)}"}
    
    @staticmethod
    def json_write(folder_path, file_name, data):
        try:
            full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), folder_path))
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            full_path = os.path.join(full_path, file_name)
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(json.dumps(data, ensure_ascii=False, indent=4))
        except:
            return False
        return True
    
    @staticmethod
    def file_append(folder_path, file_name, data):
        try:
            full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), folder_path))
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            full_path = os.path.join(full_path, file_name)
            with open(full_path, 'a', encoding='utf-8') as file:
                file.write(data + "\n")
        except:
            return False
        return True