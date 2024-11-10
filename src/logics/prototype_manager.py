from src.core.abstract_prototype import abstract_prototype
from src.core.abstract_model import abstract_model
from src.dto.filter import filter
from src.dto.filter_type import filter_type
from src.dto.matcher import matcher
from src.core.custom_raise import CustomRaise

class prototype_manager(abstract_prototype):
    def __init__(self, source: list) -> None:
        super().__init__(source)
        self.matcher = matcher()

    def create(self, data: list, filt: filter):
        self.data = self.filter_by_field(data, filt, 'name')
        self.data = self.filter_by_field(self.data, filt, 'id')
        return prototype_manager(self.data)

    def filter_by_field(self, source: list, filt: filter, field: str) -> list:
        CustomRaise.not_none_exception("item", source)
        CustomRaise.not_none_exception("filter", filt)
        CustomRaise.non_empty_exception("field", field)

        if not getattr(filt, field, None):
            return source

        result = []
        for item in source:
            if self.match_field(getattr(item, field, None), getattr(filt, field), filt.type):
                result.append(item)
            elif self.filter_checker(item, filt, field):
                result.append(item)
        return result

    def filter_checker(self, item, filt: filter, field: str) -> bool:
        CustomRaise.not_none_exception("item", item)
        CustomRaise.not_none_exception("filter", filt)
        CustomRaise.non_empty_exception("field", field)

        for attr_name in dir(item):
            attr_value = getattr(item, attr_name)
            if isinstance(attr_value, abstract_model) and self.match_field(getattr(attr_value, field, None), getattr(filt, field), filt.type):
                return True
            elif isinstance(attr_value, list):
                for inner_item in attr_value:
                    if isinstance(inner_item, abstract_model) and self.match_field(getattr(inner_item, field, None), getattr(filt, field), filt.type):
                        return True
        return False

    def match_field(self, field_value: str, filter_value: str, filter_type: filter_type) -> bool:
        if not field_value or not filter_value:
            return False

        try:
            return self.matcher.match_field(field_value, filter_value, filter_type)
        except Exception as ex:
            print(f"Ошибка: {ex}")
            return False