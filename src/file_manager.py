from src.core.custom_raise import CustomRaise
import os
import json

class file_manager():
    def json_read(self, folder_path, file_name):
        try:
            full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), folder_path))
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            full_path = os.path.join(full_path, file_name)
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                return data
            else:
                CustomRaise.not_found_exception(file_name)
        except:
            CustomRaise.operation_exception("Read file error!")
    
    def json_write(self, folder_path, file_name, data):
        try:
            full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), folder_path))
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            full_path = os.path.join(full_path, file_name)
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(json.dumps(data, ensure_ascii=False, indent=4))
        except:
            CustomRaise.operation_exception("Write file error!")
        return True