from src.core.format_reporting import format_reporting
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
            raise "набор данных пуст"
        
        ordered_fields = ["id", "name", "servings", "time", "ingredients", "instructions"]

        for row in data:
            for field in ordered_fields:
                if isinstance(row, tuple):
                    value = row[ordered_fields.index(field)]
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

        with open(os.path.join(full_path, filename + ".md"), 'w', encoding='utf-8') as file:
            file.write(self.result)