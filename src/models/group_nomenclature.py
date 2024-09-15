from src.abstract_model import abstract_model

class group_nomenclature(abstract_model):
    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)