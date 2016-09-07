from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model

from rwords.views.forms import CreateWordBookForm
from rwords.file_handler import dict_file_handler

# 创建单词书
@login_required
def create_wordbook_view(request):
    form = CreateWordBookForm()
    if request.method == 'POST':
        form = CreateWordBookForm(request.POST, request.FILES)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            dict_file_handler(request.FILES['words_file'], form.instance)
            print('上传成功')

    return render(request, 'form_template.html', context={
        'title': '创建单词书',
        'form_action': reverse('create_wordbook'),
        'form': form,
        'submit_text': '上传',
        'extra_text': '如果单词数量较多，导入单词到数据库可能需要一些时间。',
        'enctype': 'enctype=multipart/form-data'
    })
