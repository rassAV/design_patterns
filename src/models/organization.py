from src.core.abstract_model import abstract_model
from src.models.settings import settings

class organization(abstract_model):
    def __init__(self, settings: settings):
        super().__init__()
        self.inn = settings.inn
        self.bik = settings.bik
        self.account = settings.account
        self.ownership_type = settings.ownership_type
    
    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)