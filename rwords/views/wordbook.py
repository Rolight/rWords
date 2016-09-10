from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rwords.views.forms import CreateWordBookForm
from rwords.file_handler import dict_file_handler
from rwords.models import WordList, WordBook, Dict, UserProperty

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
    wordcount = wordlist.count()
    userp = get_object_or_404(UserProperty, user=request.user)

    paginator = Paginator(wordlist, 20)
    page_index = request.GET.get('page')
    try:
        wordlist = paginator.page(page_index)
    except PageNotAnInteger:
        wordlist = paginator.page(1)
    except EmptyPage:
        wordlist = paginator.page(paginator.num_pages)

    return render(request, 'wordbook.html', context={
        'wordbook': wordbook,
        'wordlist': wordlist,
        'wordcount': wordcount,
        'learning_wordbook': userp.learning_wordbook,
        'userp': userp
    })

# 查看单词书库
@login_required
def wordbook_library_view(request, id):
    wordbook_list = None
    title = ''
    id = int(id)
    if id == 0:
        wordbook_list = WordBook.objects.all()
        title = '书库'
    else:
        user = get_object_or_404(get_user_model(), pk=id)
        wordbook_list = WordBook.objects.filter(
            author=user
        )
        title = '%s上传的单词书' % user.username
    paginator = Paginator(wordbook_list, 20)
    page_index = request.GET.get('page')
    try:
        wordbook_list = paginator.page(page_index)
    except PageNotAnInteger:
        wordbook_list = paginator.page(1)
    except EmptyPage:
        wordbook_list = paginator.page(paginator.num_pages)
    userp = get_object_or_404(UserProperty, user=request.user)
    return render(request, 'wordbook_library.html', context={
        'wordbook_list': wordbook_list,
        'title': title,
        'learning_wordbook': userp.learning_wordbook,
        'userp': userp
    })

# 设置单词书
@login_required
def wordbook_set_learning_view(request, id):
    userp = get_object_or_404(UserProperty, user=request.user)
    wordbook = get_object_or_404(WordBook, pk=id)
    if userp.learning_wordbook == wordbook:
        userp.learning_wordbook = None
    else:
        userp.learning_wordbook = wordbook
    userp.save()
    return redirect(request.GET['next'])
