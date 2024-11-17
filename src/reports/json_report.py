from src.core.object_types import format_reporting
from src.core.abstract_report import abstract_report
from src.models.ingredient import ingredient
from src.models.storage import storage
from src.models.storage_transaction import storage_transaction
from src.models.recipe import recipe
from src.models.range import range
from src.models.nomenclature import nomenclature
from src.models.group_nomenclature import group_nomenclature
from src.core.custom_raise import CustomRaise
import os
import json

class json_report(abstract_report):
    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.JSON
    
    def __serialize_obj(self, obj):        
        if hasattr(obj, "to_json") and callable(getattr(obj, "to_json")):
            return obj.to_json()
        elif isinstance(obj, list):
            return [self.__serialize_obj(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.__serialize_obj(value) for key, value in obj.items()}
        elif hasattr(obj, '__dict__'):
            return {key: self.__serialize_obj(value) for key, value in obj.__dict__.items()}
        else:
            return str(obj)
    
    def create(self, data):
        if len(data) == 0:
            CustomRaise.operation_exception("Набор данных пуст")
        self.result = json.dumps(self.__serialize_obj(data), ensure_ascii=False, indent=4)

    def save(self, directory: str, filename: str):
        try:
            full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))

            if not os.path.exists(full_path):
                os.makedirs(full_path)

            with open(os.path.join(full_path, filename + self.__format.value), 'w', encoding='utf-8') as file:
                file.write(self.result)
            return True
        except:
            return False