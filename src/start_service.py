from src.core.abstract_logic import abstract_logic
from src.storage_reposity import storage_reposity
from src.models.range import range
from src.models.group_nomenclature import group_nomenclature
from src.models.nomenclature import nomenclature
from src.settings_manager import settings_manager
from src.models.settings import settings
from src.core.custom_raise import CustomRaise
from src.models.ingredient import ingredient
from src.models.recipe import recipe

import os
import re

class start_service(abstract_logic):
    __reposity: storage_reposity = None
    __settings_manager: settings_manager = None

    def __init__(self, reposity : storage_reposity, manager: settings_manager) -> None:
        super().__init__()
        CustomRaise.type_exception("reposity", reposity, storage_reposity)
        self.__reposity = reposity
        self.__settings_manager = manager

    @property
    def settings(self) -> settings:
        return self.__settings_manager.settings
    
    @property
    def data(self):
        return self.__reposity.data
    
    def __create_unit_measurements(self):
        units = [
            range(),
            range("килограмм", 1000, range()),
            range("тонна", 1000, range("килограмм", 1000)),
            range("милилитр", 1),
            range("литр", 1000, range("милилитр", 1))
        ]
        self.__reposity.data[storage_reposity.ranges_key()] = units
    
    def __create_nomenclature_group(self):
        list = [ group_nomenclature.default_group_source(), group_nomenclature.default_group_cold() ]
        self.__reposity.data[storage_reposity.groups_key()] = list
    
    def __create_nomenclature(self):
        nomenclatures = [
            nomenclature("Мука", group_nomenclature.default_group_source(), range("килограмм", 1000, range())),
            nomenclature("Замороженные овощи", group_nomenclature.default_group_cold(), range("килограмм", 1000, range()))
        ]
        self.__reposity.data[storage_reposity.nomenclature_key()] = nomenclatures

    def __create_receipts(self):
        receipts = []
        docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs"))

        # if not os.path.exists(docs_path):
        #     raise FileNotFoundError(f"Директория {docs_path} не найдена.")
        
        for filename in os.listdir(docs_path):
            if filename.endswith(".md"):
                with open(os.path.join(docs_path, filename), 'r', encoding='utf-8') as file:
                    name = ""
                    servings = ""
                    ing_name = ""
                    ing_unit_value = 1
                    ing_unit_name = ""
                    ingredients = []
                    time = ""
                    instructions = []

                    for line in file:
                        line = line.strip()

                        if line.startswith("# "):
                            name = line[2:].strip()

                        if line.startswith("#### "):
                            servings = line[5:].strip()

                        if line.startswith("| ") and not line.startswith("| Ингредиенты"):
                            line = line[2:].strip()

                            ing_name = line.split("|")[0].strip()
                            ing_unit_value = line.split("|")[1].split(" ")[1].strip()
                            ing_unit_name = line.split("|")[1].split(" ")[2].strip()

                            ingredients.append(ingredient(ing_name, int(ing_unit_value), ing_unit_name))

                        if line.startswith("Время приготовления: "):
                            time = line[21:].strip()

                        if re.match(r'^\d+\.\s', line):
                            instructions.append(line.strip())

                    receipts.append(recipe(name, servings, ingredients, time, instructions))
        self.__reposity.data[storage_reposity.receipts_key()] = receipts

    def create(self):
        self.__create_unit_measurements()
        self.__create_nomenclature_group()
        self.__create_nomenclature()
        self.__create_receipts()

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)