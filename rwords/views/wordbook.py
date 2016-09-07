from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model

from rwords.views.forms import CreateWordBookForm
from rwords.file_handler import dict_file_handler
from rwords.models import WordList, WordBook, Dict

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
            return redirect(reverse('wordbook', args=[form.instance.id]))

    return render(request, 'form_template.html', context={
        'title': '创建单词书',
        'form_action': reverse('create_wordbook'),
        'form': form,
        'submit_text': '上传',
        'extra_text': '如果单词数量较多，导入单词到数据库可能需要一些时间。',
        'enctype': 'enctype=multipart/form-data'
    })

# 查看单词书
@login_required
def wordbook_view(request, id):
    wordbook = get_object_or_404(WordBook, pk=id)
    wordlist = WordList.objects.filter(wordbook=wordbook)
    return render(request, 'wordbook.html', context={
        'wordbook': wordbook,
        'wordlist': wordlist
    })


