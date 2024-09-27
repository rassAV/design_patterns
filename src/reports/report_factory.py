from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.settings_manager import settings_manager
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.reports.md_report import md_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.docx_report import docx_report
from src.reports.xlsx_report import xlsx_report
from src.core.custom_raise import CustomRaise

class report_factory(abstract_logic):
    __reports: dict = {}

    def __init__(self) -> None:
        super().__init__()
        self.__reports[ format_reporting.CSV ] = csv_report
        self.__reports[ format_reporting.MD ] = md_report
        self.__reports[ format_reporting.JSON ] = json_report
        self.__reports[ format_reporting.XML ] = xml_report
        self.__reports[ format_reporting.DOCX ] = docx_report
        self.__reports[ format_reporting.XLSX ] = xlsx_report
    
    def create(self, manager: settings_manager) ->  abstract_report:
        format = manager.settings.report_format
        CustomRaise.type_exception("format", format, format_reporting)
        
        if format not in self.__reports.keys():
            self.set_exception( CustomRaise.operation_exception(f"Указанный вариант формата {format} не реализован!"))
        
        report = self.__reports[format]
        return report()
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)