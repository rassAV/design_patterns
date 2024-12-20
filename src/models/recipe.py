from src.core.abstract_model import abstract_model
from src.models.ingredient import ingredient
from src.core.custom_raise import CustomRaise

class recipe(abstract_model):
    __name: str = "default"
    __servings: str = ""
    __ingredients: list = []
    __time: str = ""
    __instructions: list = []

    def __init__(self, name: str = "default", servings: str = "", ingredients: list = [], time: str = "", instructions: list = []):
        super().__init__()
        CustomRaise.type_exception("name", name, str)
        CustomRaise.type_exception("servings", servings, str)
        CustomRaise.type_exception("ingredients", ingredients, list)
        CustomRaise.type_exception("time", time, str)
        CustomRaise.type_exception("instructions", instructions, list)
        self.__name = name
        self.__servings = servings
        self.__ingredients = ingredients
        self.__time = time
        self.__instructions = instructions

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "servings": self.servings,
            "ingredients": [ingredient.to_json() for ingredient in self.ingredients],
            "time": self.time,
            "instructions": self.instructions,
        }

    @staticmethod
    def from_json(data):
        return recipe(
            name=data.get("name"),
            servings=data.get("servings"),
            ingredients=[ingredient.from_json(item) for item in data.get("ingredients", [])],
            time=data.get("time"),
            instructions=data.get("instructions", []),
        )
    
    def __str__(self):
        return f"Recipe(name: {self.name}, servings: {self.servings}, ingredients_counts: {len(self.ingredients)}, time: {self.time}, instructions_counts: {len(self.instructions)})"

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        CustomRaise.type_exception("name", name, str)
        self.__name = name.strip()

    @property
    def servings(self) -> str:
        return self.__servings
    
    @servings.setter
    def servings(self, servings):
        CustomRaise.type_exception("servings", servings, str)
        self.__servings = servings
    
    @property
    def ingredients(self) -> str:
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, ingredients):
        CustomRaise.type_exception("ingredients", ingredients, list)
        self.__ingredients = ingredients

    @property
    def time(self) -> str:
        return self.__time
    
    @time.setter
    def time(self, time):
        CustomRaise.type_exception("time", time, str)
        self.__time = time

    @property
    def instructions(self) -> str:
        return self.__instructions
    
    @instructions.setter
    def instructions(self, instructions):
        CustomRaise.type_exception("instructions", instructions, list)
        self.__instructions = instructions

    def set_compare_mode(self, other) -> bool:
        return super().set_compare_mode(other)