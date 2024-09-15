import unittest
from src.settings_manager import settings_manager

class test_settings(unittest.TestCase):
   def test_settings_manager_open(self):
      # Подготовка
      manager1 = settings_manager()

      # Проверки 
      assert manager1.open("settings (default).json", "../") is True

   def test_settings_manager_open_fail(self):
      # Подготовка
      manager1 = settings_manager()
      manager1.open("../53453.json")

      # Проверки 
      print(manager1.error_text)
      assert manager1.is_error == True

   def test_settings_manager_singletone(self):
      # Подготовка
      manager1 = settings_manager()
      manager1.open("settings (default).json", "../")
      manager2 = settings_manager()

      # Проверки
      assert manager1.settings.inn == manager2.settings.inn
      assert manager1.settings.account == manager2.settings.account
      assert manager1.settings.correspondent_account == manager2.settings.correspondent_account
      assert manager1.settings.bik == manager2.settings.bik
      assert manager1.settings.organization_name == manager2.settings.organization_name
      assert manager1.settings.ownership_type == manager2.settings.ownership_type