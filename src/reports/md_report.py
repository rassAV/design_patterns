from src.core.object_types import format_reporting
from src.core.abstract_report import abstract_report
from src.core.custom_raise import CustomRaise

import os

class md_report(abstract_report):
    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.MD
    
    def create(self, data: list):
        CustomRaise.type_exception("data", data, list)
        if len(data) == 0:
            CustomRaise.operation_exception("Набор данных пуст")
        
        first_model = data[0]
        
        if isinstance(first_model, tuple):
            fields = [f"column_{i}" for i in range(len(first_model))]
        else:
            fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model, x)), dir(first_model)))

        for row in data:
            for field in fields:
                if isinstance(row, tuple):
                    value = row[fields.index(field)]
                else:
                    value = getattr(row, field)
                    
                if field in ["ingredients", "instructions"] and isinstance(value, list):
                    self.result += f"**{str(field)}**:\n"
                    for item in value:
                        self.result += f"- {str(item)}\n"
                else:
                    self.result += f"**{str(field)}**: {str(value)}\n"
            self.result += "\n"
        
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