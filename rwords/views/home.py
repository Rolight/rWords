from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rwords.models import UserProperty

@login_required
def home_page(request):
    userp = get_object_or_404(UserProperty, user=request.user)
    return render(request, 'home.html', context={'userp': userp})
