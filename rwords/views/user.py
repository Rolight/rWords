from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def login_page(request):
    return render(request, 'login.html')
