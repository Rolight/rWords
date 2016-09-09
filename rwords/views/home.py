from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from rwords.models import UserProperty, LearnTask, Dict

@login_required
def home_page(request):
    userp = get_object_or_404(UserProperty, user=request.user)
    LearnTask.get_user_tasks(request.user)
    return render(request, 'home.html', context={'userp': userp})

# 单词查询界面
@login_required
def word_view(request):
    word = None
    if request.method == 'GET' and 'word' in request.GET:
        word = Dict.objects.filter(text=request.GET['word']).first()
    return render(request, 'word.html', context={'word': word})
