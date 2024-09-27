from src.core.abstract_model import abstract_model

class group_nomenclature(abstract_model):
    @staticmethod
    def default_group_source():
        item = group_nomenclature()
        item.name = "Сырьё"
        return item
    
    @staticmethod
    def default_group_cold():
        item = group_nomenclature()
        item.name = "Заморозка"
        return item

    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)