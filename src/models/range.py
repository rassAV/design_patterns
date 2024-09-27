from src.core.abstract_model import abstract_model
from src.core.custom_raise import CustomRaise

class range(abstract_model):
    def __init__(self, unit_range: str = "грамм", conversion_factor: int = 1, base_range: range = None):
        if base_range is not None:
            CustomRaise.value_required_exception(base_range.conversion_factor, conversion_factor)
        CustomRaise.type_exception("unit_range", unit_range, str)
        CustomRaise.type_exception("conversion_factor", conversion_factor, int)
        self.unit_range = unit_range
        self.conversion_factor = conversion_factor
        self.base_range = base_range
    
    def set_compare_mode(self, other) -> bool:
        if other is None or not isinstance(other, range): return False
        return self.name == other.name