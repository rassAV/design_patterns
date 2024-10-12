from src.core.custom_exception import OperationException, TypeException, NonEmptyException, NotNoneException, LengthExceededException, LengthRequiredException, ValueRequiredException, FactorRequiredException, NotFoundException

class CustomRaise:
    @staticmethod
    def operation_exception(text: str):
        raise OperationException(text)

    @staticmethod
    def type_exception(argument_name: str, value, required_type):
        if not isinstance(value, required_type):
            raise TypeException(argument_name, required_type)
        
    @staticmethod
    def non_empty_exception(argument_name: str, value: str):
        if not value.strip():
            raise NonEmptyException(argument_name)
        
    @staticmethod
    def not_none_exception(argument_name: str, value):
        if value is None:
            raise NotNoneException(argument_name)

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