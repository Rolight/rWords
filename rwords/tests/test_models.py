from django.test import TestCase
from django.db.utils import IntegrityError

# Create your tests here.
from rwords.models import Dict

# 词库模型测试
class DictModelTest(TestCase):
    # 测试默认值
    def test_default_text(self):
        dt = Dict(text='apple')
        dt.save()
        self.assertEqual(dt.example_set.count(), 0)
        self.assertEqual(dt.synonym_set.count(), 0)
        dt.example_set.create(text='eat apple')
        dt.synonym_set.create(text='leppa')
        self.assertEqual(dt.example_set.first().text, 'eat apple')
        self.assertEqual(dt.synonym_set.first().text, 'leppa')

    # 测试唯一性
    def test_unique_text(self):
        dt = Dict(text='apple')
        dt.save()
        with self.assertRaises(IntegrityError):
            dt1 = Dict(text='apple')
            dt1.save()
