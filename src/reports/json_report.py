from src.core.object_types import format_reporting
from src.core.object_types import transaction_type
from src.core.abstract_report import abstract_report
from src.models.ingredient import ingredient
from src.core.custom_raise import CustomRaise
from datetime import datetime
import os
import json

class json_report(abstract_report):
    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.JSON
        # self.__seen_objects = set()
    
    def __serialize_obj(self, obj):
        # if id(obj) in self.__seen_objects:
        #     return f"<Circular reference to object id {id(obj)}>"
        # self.__seen_objects.add(id(obj))
        
        if isinstance(obj, ingredient):
            return {
                "name": obj.name,
                "unit_value": obj.unit_value,
                "range": {
                        "unit_range": obj.nomenclature.range.unit_range,
                        "conversion_factor": obj.nomenclature.range.conversion_factor,
                        "base_range": obj.nomenclature.range.base_range
                    },
                "nomenclature": {
                    "full_name": obj.nomenclature.full_name,
                    "group": {
                        "name": obj.nomenclature.group.name
                    },
                    "range": {
                        "unit_range": obj.nomenclature.range.unit_range,
                        "conversion_factor": obj.nomenclature.range.conversion_factor,
                        "base_range": obj.nomenclature.range.base_range
                    }
                }
            }
        elif isinstance(obj, list):
            return [self.__serialize_obj(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, transaction_type):
            return obj.value
        elif hasattr(obj, '__dict__'):
            return {key: self.__serialize_obj(value) for key, value in obj.__dict__.items()}
        else:
            return str(obj)
    
    def create(self, data: list):
        CustomRaise.type_exception("data", data, list)
        if len(data) == 0:
            CustomRaise.operation_exception("Набор данных пуст")

        serializable_data = [self.__serialize_obj(row) for row in data]
        self.result = json.dumps(serializable_data, ensure_ascii=False, indent=4)

    def save(self, directory: str, filename: str):
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))

        if not os.path.exists(full_path):
            os.makedirs(full_path)

        try:
            with open(os.path.join(full_path, filename + self.__format.value), 'w', encoding='utf-8') as file:
                file.write(self.result)
            return True
        except:
            return False