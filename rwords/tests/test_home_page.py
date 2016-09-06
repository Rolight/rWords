from django.test import TestCase

from rwords.views.home import home_page

# 主页视图测试
class TestHomePage(TestCase):

    # 测试没有登陆时是否能够正常跳转到登陆界面
    def test_redirect_while_not_logged(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/')

