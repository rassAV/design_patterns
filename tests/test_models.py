import unittest
from src.models.nomenclature import nomenclature
from src.models.range import range
from src.models.group_nomenclature import group_nomenclature
from src.models.storage import storage
from src.models.organization import organization
from src.settings_manager import settings_manager

class test_models(unittest.TestCase):
   def test_compare_model(self):
      # Подготовка
      n1 = nomenclature()
      n1.full_name = "test1"
      n2 = nomenclature()
      n2.full_name = "test1"

      g_n1 = group_nomenclature()
      g_n1.name = "g_n"
      g_n2 = group_nomenclature()
      g_n2.name = "g_n"

      st1 = storage()
      st2 = storage()

      range1 = range()
      range1.name = "1"
      range2 = range()
      range2.name = "1"
      
      # Проверка
      assert n1 != n2
      assert g_n1 != g_n2
      assert st1 != st2
      assert range1 == range2

   def test_range_model(self):
      # Подготовка
      base_range = range("грамм", 1)
      new_range = range("килограмм", 1000, base_range)

      # Проверка
      assert new_range.unit_range == "килограмм" and new_range.conversion_factor == 1000
      assert new_range.base_range.unit_range == "грамм" and new_range.base_range.conversion_factor == 1

   def test_organization_model(self):
      # Подготовка
      manager = settings_manager()
      manager.open("settings (default).json", "../")
      org = organization(manager.settings)

      # Проверка
      assert org.inn == manager.settings.inn
      assert org.bik == manager.settings.bik
      assert org.account == manager.settings.account
      assert org.ownership_type == manager.settings.ownership_type

   def test_nomenclature_model(self):
      # Подготовка
      n = nomenclature()
      n.full_name = "test1"
      n.range = range("килограмм", 1000, range())

      # Проверка
      assert n.full_name == "test1"
      assert n.range.unit_range == "килограмм" and n.range.conversion_factor == 1000
      assert n.range.base_range.unit_range == "грамм" and n.range.base_range.conversion_factor == 1