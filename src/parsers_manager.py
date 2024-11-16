from src.core.abstract_logic import abstract_logic
from src.storage_reposity import storage_reposity
from src.models.range import range
from src.models.group_nomenclature import group_nomenclature
from src.models.nomenclature import nomenclature
from src.models.ingredient import ingredient
from src.models.recipe import recipe
from src.core.custom_raise import CustomRaise

import os
import re
import json

class parsers_manager(abstract_logic):
    def parse_md_receipts():
        receipts = []
        docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/recipes"))

        if not os.path.exists(docs_path):
            CustomRaise.operation_exception(f"Директория {docs_path} не найдена.")
        
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

                            ingredients.append(ingredient(ing_name, int(ing_unit_value), range(ing_unit_name, 1, None), nomenclature(ing_name, group_nomenclature.default_group_source(), range(ing_unit_name, 1, None))))

                        if line.startswith("Время приготовления: "):
                            time = line[21:].strip()

                        if re.match(r'^\d+\.\s', line):
                            instructions.append(line.strip())

                    receipts.append(recipe(name, servings, ingredients, time, instructions))
        return receipts
    
    def parse_json_recipe(data: dict) -> recipe:
        return recipe(
            name=data.get('_recipe__name', 'default'),
            servings=data.get('_recipe__servings', ''),
            ingredients=[parsers_manager.parse_json_ingredient(ing) for ing in data.get('_recipe__ingredients', [])],
            time=data.get('_recipe__time', ''),
            instructions=data.get('_recipe__instructions', [])
        )

    def parse_json_ingredient(data: dict) -> ingredient:
        return ingredient(
            name=data.get('name', 'default'),
            unit_value=data.get('unit_value', 1),
            rng=parsers_manager.parse_json_range(data.get('range', {})),
            product=parsers_manager.parse_json_nomenclature(data.get('nomenclature', {}))
        )

    def parse_json_nomenclature(data: dict) -> nomenclature:
        return nomenclature(
            full_name=data.get('full_name', 'default'),
            group=parsers_manager.parse_json_group_nomenclature(data.get('group', {})),
            rng=parsers_manager.parse_json_range(data.get('range', {}))
        )

    def parse_json_range(data: dict) -> range:
        return range(
            unit_range=data.get('unit_range', 'грамм'),
            conversion_factor=data.get('conversion_factor', 1),
            base_range=parsers_manager.parse_json_range(data.get('base_range', None)) if data.get('base_range') else None
        )

    def parse_json_group_nomenclature(data: dict) -> group_nomenclature:
        return group_nomenclature(
            name=data.get('name', '')
        )

    def parse_json(file_name: str, file_path: str = "../data/reports") -> list:
        full_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), file_path)), file_name)
        with open(full_path, 'r', encoding='utf-8') as json_data:
            data = json.load(json_data)
        
            if isinstance(data, list) and len(data) == 0:
                return []

            first_item = data[0]

            if 'unit_range' in first_item:
                return [parsers_manager.parse_json_range(item) for item in data]
            elif 'full_name' in first_item:
                return [parsers_manager.parse_json_nomenclature(item) for item in data]
            elif 'name' in first_item and len(first_item.keys()) == 1:
                return [parsers_manager.parse_json_group_nomenclature(item) for item in data]
            elif '_recipe__name' in first_item:
                return [parsers_manager.parse_json_recipe(item) for item in data]
            else:
                CustomRaise.operation_exception("Неизвестный тип данных в JSON.")
    
    def set_exception(self, e: Exception):
        self._inner_set_exception(e)
    
    def handle_event(self, type, params):
        super().handle_event(type, params)