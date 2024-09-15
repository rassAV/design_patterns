from src.custom_exception import TypeException, LengthExceededException, LengthRequiredException, ValueRequiredException, FactorRequiredException, NotFoundException

class CustomRaise:        
    @staticmethod
    def type_exception(argument_name: str, value, required_type):
        if not isinstance(value, required_type):
            raise TypeException(argument_name, required_type)

    @staticmethod
    def length_exceeded_exception(argument_name: str, value: str, max_length: int):
        if len(value) > max_length:
            raise LengthExceededException(argument_name, len(value), max_length)
        
    @staticmethod
    def length_required_exception(argument_name: str, value: str, required_length: int):
        if len(value) != required_length:
            raise LengthRequiredException(argument_name, len(value), required_length)
    
    @staticmethod
    def value_required_exception(value: int, new_value: int):
        if value > new_value:
            raise ValueRequiredException(value, new_value)
        
    @staticmethod
    def factor_required_exception(value: int):
        if value > 0:
            raise FactorRequiredException(value)

    @staticmethod
    def not_found_exception(file_name: str):
        raise NotFoundException(file_name)