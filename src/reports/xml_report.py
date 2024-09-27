from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.custom_raise import CustomRaise

import os

class xml_report(abstract_report):
    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.XML
    
    def create(self, data: list):
        CustomRaise.type_exception("data", data, list)
        if len(data) == 0:
            raise "набор данных пуст"
        
        ordered_fields = ["id", "name", "servings", "time", "ingredients", "instructions"]

        self.result = "<root>\n"
        for row in data:
            self.result += "  <item>\n"
            for field in ordered_fields:
                if isinstance(row, tuple):
                    value = row[ordered_fields.index(field)]
                else:
                    value = getattr(row, field)

                # Обработка списков для ingredients и instructions
                if field in ["ingredients", "instructions"] and isinstance(value, list):
                    self.result += f"    <{field}>\n"
                    for item in value:
                        self.result += f"      <element>{str(item)}</element>\n"  # Каждый элемент в новом теге <element>
                    self.result += f"    </{field}>\n"
                else:
                    self.result += f"    <{field}>{str(value)}</{field}>\n"

            self.result += "  </item>\n"
        self.result += "</root>"

    def save(self, directory: str, filename: str):
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))

        if not os.path.exists(full_path):
            os.makedirs(full_path)

        with open(os.path.join(full_path, filename + ".xml"), 'w', encoding='utf-8') as file:
            file.write(self.result)