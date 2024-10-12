from src.dto.filter_type import filter_type
from src.core.custom_raise import CustomRaise

class matcher:
    def __init__(self):
        self.matching_functions = {ft: getattr(self, ft.name.lower()) for ft in filter_type}

    def match_field(self, field_value: str, filter_value: str, filter_type: filter_type) -> bool:
        if filter_type in self.matching_functions:
            return self.matching_functions[filter_type](field_value, filter_value)
        return False

    def equals(self, field_value: str, filter_value: str) -> bool:
        CustomRaise.non_empty_exception("field_value", field_value)
        CustomRaise.non_empty_exception("filter_value", filter_value)
        return field_value == filter_value

    def like(self, field_value: str, filter_value: str) -> bool:
        CustomRaise.non_empty_exception("field_value", field_value)
        CustomRaise.non_empty_exception("filter_value", filter_value)
        return filter_value in field_value

    def greater_than(self, field_value: str, filter_value: str) -> bool:
        CustomRaise.non_empty_exception("field_value", field_value)
        CustomRaise.non_empty_exception("filter_value", filter_value)
        return float(field_value) > float(filter_value)

    def less_than(self, field_value: str, filter_value: str) -> bool:
        CustomRaise.non_empty_exception("field_value", field_value)
        CustomRaise.non_empty_exception("filter_value", filter_value)
        return float(field_value) < float(filter_value)

    def in_range(self, field_value: str, filter_value: str) -> bool:
        CustomRaise.non_empty_exception("field_value", field_value)
        CustomRaise.non_empty_exception("filter_value", filter_value)
        min_val, max_val = map(float, filter_value.split(","))
        return min_val <= float(field_value) <= max_val