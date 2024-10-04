from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.custom_raise import CustomRaise

import os

class csv_report(abstract_report):
    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.CSV
    
    def create(self, data: list):
        CustomRaise.type_exception("data", data, list)
        if len(data) == 0:
            CustomRaise.operation_exception("Набор данных пуст")
        
        first_model = data[0]

        if isinstance(first_model, tuple):
            fields = [f"column_{i}" for i in range(len(first_model))]
        else:
            fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model, x )),  dir(first_model) ))

        for field in fields:
            self.result += f"{str(field)};"

        self.result += "\n"

        for row in data:
            if isinstance(row, tuple):
                for value in row:
                    self.result += f"{str(value)};"
            else:
                for field in fields:
                    value = getattr(row, field)
                    if isinstance(value, list):
                        self.result += f"[{', '.join([str(item) for item in value])}];"
                    else:
                        self.result += f"{str(value)};"
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