"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from .views.home import home_page
from .views.user import login_view, register_view, logout_view
from .views.wordbook import create_wordbook_view, wordbook_view, wordbook_library_view


urlpatterns = [
    url(r'^$', home_page, name='home_page'),
    url(r'^user/login/$', login_view, name='login'),
    url(r'^user/register/$', register_view, name='register'),
    url(r'^user/logout/$', logout_view, name='logout'),
    url(r'^wordbook/new/$', create_wordbook_view, name='create_wordbook'),
    url(r'^wordbook/(\d+)/$', wordbook_view, name='wordbook'),
    url(r'^wordbook/library/(\d+)/$', wordbook_library_view, name='wordbook_library')
]
