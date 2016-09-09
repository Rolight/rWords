from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest

from unittest import skip

from rwords.views.home import home_page

# 主页视图测试
class TestHomePage(TestCase):

    # 测试没有登录时是否能够正常跳转到登录界面
    def test_redirect_while_not_log_in(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/')


    # 测试登录后是否能够停留在主页
    # = =
    # 有时间改用mock重写
    @skip
    def test_redirect_after_logging(self):
        user = User.objects.create_user(username='user', password='password')
        request = HttpRequest()
        request.user = user
        user.is_authenticate = True
        response = home_page(request)
        self.assertEqual(response.status_code, 200)


