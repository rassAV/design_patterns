from src.core.abstract_logic import abstract_logic
from src.core.custom_raise import CustomRaise
from src.core.object_types import event_type
from src.log_manager import log_manager

class observe_service:
    observers = []

    @staticmethod
    def append(service: abstract_logic):
        if service is None:
            return
        if not isinstance(service, abstract_logic):
            raise CustomRaise.operation_exception("Некорректный тип данных!")

        services_names = list(map(lambda x: type(x).__name__, observe_service.observers))
        found = type(service).__name__ in services_names
        if not found:
            observe_service.observers.append(service)

    @staticmethod
    def raise_event(event_type: event_type, logs: log_manager, params):
        statuses = {}
        for service in observe_service.observers:
            if service is not None:
                class_name = type(service).__name__
                status = service.handle_event(event_type, logs, params)
                statuses[class_name] = status
        return statuses