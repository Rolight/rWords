from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

from rwords.views.forms import RegisterForm, LoginForm

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid() and form.get_user():
            login(request, form.get_user())
            return redirect(reverse('home_page'))
    return render(request, 'login.html', context={'form': form})

def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login_page'))
    return render(request, 'register.html', context={'form': form})
