from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model

from rwords.views.forms import (
    RegisterForm, LoginForm, LearningSettingsForm,
    NoteForm, UserPassWordChangeForm
)
from rwords.models import UserProperty, LearnTask, Note, LearnState

import copy


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

# 学习设置
@login_required
def learning_settings_view(request):
    userp = get_object_or_404(UserProperty, user=request.user)
    form = LearningSettingsForm()
    if request.method == 'POST':
        form = LearningSettingsForm(data=request.POST)
        if form.is_valid():
            userp.amount = form.cleaned_data['amount']
            userp.save()
            return redirect(reverse('learning_settings'))
    return render(request, 'learning_settings.html', context={
        'userp': userp,
        'form': form,
        'all': 0
    })

# 学习页面
@login_required
def learning_view(request):
    task = LearnTask.get_user_tasks(request.user).first()
    userp = get_object_or_404(UserProperty, user=request.user)
    if task is None:
        redirect(reverse('home_page'))
    if request.method == 'GET':
        if not task:
            return redirect(reverse('home_page'))
        return render(request, 'learning.html', context={
            'wordlist': task.word,
            'userp': userp,
            'task': task
        })
    elif request.method == 'POST':
        # 判断类型
        form = NoteForm()
        alert_text = ''
        alert_type = 'info'
        if 'add-note' not in request.POST:
            # 如果不是提交笔记
            # 先把任务顺序改变
            # 根据post类型进行相应操作
            if 'too-simple' in request.POST:
                task.too_simple()
                alert_text = '你已将该单词标记为太简单，将不会再对这个单词进行学习'
            elif 'unknown' in request.POST:
                task.unknown()
                alert_text = '稍后将重新学习这个单词'
            elif 'known' in request.POST:
                task.known()
                if task.finished:
                    alert_text = '这个单词学习完成，今天将不再出现'
                    alert_type = 'success'
                else:
                    alert_text = '这个单词稍后还需要复习一遍'
        else:
            # 添加笔记
            try:
                task_id = int(request.POST['task_id'])
                task = LearnTask.objects.get(id=task_id)
            except:
                raise Http404
            form = NoteForm(data=request.POST)
            if form.is_valid():
                Note.objects.create(
                    userproperty=userp,
                    word=task.word,
                    content=form.cleaned_data['content'],
                    shared=form.cleaned_data['shared']
                )
                alert_text = '笔记添加成功'

        return render(request, 'learning_detail.html', context={
            'wordlist': task.word,
            'userp': userp,
            'form': form,
            'task': task,
            'alert_text': alert_text,
            'alert_type': alert_type,
            'my_notes': task.word.user_notes(request.user),
            'shared_notes': task.word.shared_notes(exclude_user=request.user)
        })

# 我的词库页面
@login_required
def learning_state_view(request):
    userp = get_object_or_404(UserProperty, user=request.user)
    return render(request, 'learning_state.html', context={
        'learnstates': userp.learnstates()
    })

# 忘记单词
@login_required
def learning_state_forget_view(request, id):
    state = get_object_or_404(LearnState, pk=id)
    state.forgot()
    return redirect(request.GET['next'])

# 浏览笔记
@login_required
def user_notes_view(request):
    return render(request, 'user_notes.html', context={
        'userp': get_object_or_404(UserProperty, user=request.user)
    })

# 编辑笔记
@login_required
def user_notes_edit_view(request, id):
    form = NoteForm()
    note = get_object_or_404(Note, pk=id)
    if request.method == 'GET':
        form = NoteForm(initial={
            'content': note.content,
            'shared': note.shared
        })
        context = {'form': form, 'note': note}
        if 'alter' in request.GET:
            context['alter'] = 'alter'
        return render(request, 'user_notes_edit.html', context=context)
    elif 'alter' in request.POST:
        form = NoteForm(data=request.POST)
        if form.is_valid():
            note.shared = form.cleaned_data['shared']
            note.content = form.cleaned_data['content']
            note.save()
            return redirect(reverse('user_notes_edit', args=[note.id, ]) + '?alter=1')
        return redirect(reverse('user_notes_edit'), args=[note.id, ])
    elif 'delete' in request.POST:
        note.delete()
        return redirect(reverse('user_notes'))
    raise Http404

# 修改密码
@login_required
def change_password_view(request):
    context = {
        'title': '修改密码',
        'submit_text': '确认修改',
        'form_action': reverse('change_password')
    }
    form = UserPassWordChangeForm(request.user)
    if request.method == 'POST':
        form = UserPassWordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home_page'))
    context['form'] = form
    return render(request, 'form_template.html', context=context)




