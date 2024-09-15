from src.settings_manager import settings_manager

manager1 = settings_manager()
manager1.open("settings1.json")
print(f"settings1: {manager1.settings.inn}")

manager2 = settings_manager()
manager2.open("settings2.json")
print(f"settings2: {manager2.settings.inn}")