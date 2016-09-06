from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest

from rwords.views.home import home_page

class test_view_user(TestCase):

    # 测试能否正常登陆
    def test_register(self):
        pass


