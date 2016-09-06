from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your tests here.
from rwords.models import Dict, Example, Synonym
from rwords.models import WordBook, WordList, UserProperty
from rwords.models import Note, LearnState

# 主页视图测试
class TestHomePage(TestCase):
    pass
