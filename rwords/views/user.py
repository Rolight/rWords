from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model

from rwords.views.forms import RegisterForm, LoginForm


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid() and form.get_user():
            login(request, form.get_user())
            return redirect(reverse('home_page'))
    return render(request, 'form_template.html', context={
        'title': '用户登录',
        'form': form,
        'form_action': reverse('login'),
        'submit_text': '登录'
    })


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    return render(request, 'form_template.html', context={
        'title': '用户注册',
        'form': form,
        'form_action': reverse('register'),
        'submit_text': '注册'
    })

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('home_page'))


