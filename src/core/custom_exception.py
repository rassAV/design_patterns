class CustomException(Exception):
    pass

class OperationException(CustomException):
    def __init__(self, text: str):
        self.message = f"{text}"
        super().__init__(self.message)

class TypeException(CustomException):
    def __init__(self, argument_name: str, required_type: int):
        self.message = f"Некорректно передан параметр! Аргумент {argument_name} ожидает тип {required_type}!"
        super().__init__(self.message)

class NonEmptyException(CustomException):
    def __init__(self, argument_name: str):
        self.message = f"Значение аргумента {argument_name} не должно быть пустым!"
        super().__init__(self.message)

class NotNoneException(CustomException):
    def __init__(self, argument_name: str):
        self.message = f"Значение аргумента {argument_name} не должно быть None!"
        super().__init__(self.message)

class LengthExceededException(CustomException):
    def __init__(self, argument_name: str, value_length: int, max_length: int):
        self.message = f"Некорректно передан параметр! Аргумент {argument_name} длинной {value_length} превышает лимит в {max_length} символов!"
        super().__init__(self.message)

class LengthRequiredException(CustomException):
    def __init__(self, argument_name: str, value_length: int, required_length: int):
        self.message = f"Некорректно передан параметр! Аргумент {argument_name} длинной {value_length} должен быть равен длинне {required_length} символов!"
        super().__init__(self.message)

class ValueRequiredException(CustomException):
    def __init__(self, value: int, new_value: int):
        self.message = f"Некорректно передан параметр! Коэффициент пересчёта {new_value} должен быть больше, базового коэффициента пересчёта {value}"
        super().__init__(self.message)

class FactorRequiredException(CustomException):
    def __init__(self, value: int):
        self.message = f"Некорректно передан параметр! Коэффициент пересчёта {value} должен быть больше нуля!"
        super().__init__(self.message)

class NotFoundException(CustomException):
    def __init__(self, file_name: str):
        self.message = f"Файл {file_name} не найден!\nУстановлены настройки по умолчанию!"
        super().__init__(self.message)