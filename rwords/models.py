from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

import math
import random
from datetime import datetime


# Create your models here.
class UserProperty(models.Model):
    # 关联的用户
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 正在学习的单词书
    learning_wordbook = models.ForeignKey('WordBook', on_delete=None, null=True, default=None)
    # 每日学习量
    amount = models.IntegerField(null=False, default=50)
    # 笔记
    notes = models.ManyToManyField('WordList', related_name='note_users', through='Note')
    # 学习记录
    states = models.ManyToManyField('WordList', related_name='learn_users', through='LearnState')
    # 学习任务
    tasks = models.ManyToManyField('WordList', related_name='learn_task_users', through='LearnTask')

    def __str__(self):
        return self.user.username

    # 待学习单词
    def unknown_words(self):
        unknown_words = []
        # 如果用户有单词书
        if self.learning_wordbook:
            learned_words = self.states.all()
            book_words = self.learning_wordbook.wordlist_set.all()
            unknown_words = [word for word in book_words if word not in learned_words]
        return unknown_words

    # 待复习单词
    def review_words(self):
        return [s.word for s in self.learnstate_set.all() if not (s.master or s.too_simple)]

# 词库
class Dict(models.Model):
    text = models.TextField(null=False, unique=True, default='')

    def __str__(self):
        return self.text


# 例句
class Example(models.Model):
    word = models.ForeignKey(Dict, on_delete=models.CASCADE)
    text_eng = models.TextField(null=False, default='')
    text_chs = models.TextField(null=False, default='')


# 近义词
class Synonym(models.Model):
    word = models.ForeignKey(Dict, on_delete=models.CASCADE)
    text = models.TextField(null=False, default='')


# 单词书
class WordBook(models.Model):
    # 创建日期
    pub_date = models.DateField(auto_now_add=True, editable=False)
    # 更新日期
    update_date = models.DateField(auto_now=True, editable=False)
    # 作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 单词书名称
    name = models.CharField(verbose_name='单词书名称', max_length=150, default='')
    # 单词表
    words = models.ManyToManyField(Dict, through='WordList')
    # 封面
    image = models.ImageField(upload_to='bookfront/%Y/%m/%d', verbose_name='封面图片')

    def __str__(self):
        return '%s from %s' % (self.name, self.author.username)

    def get_absolute_url(self):
        reverse('wordbook', args=[self.id, ])


class WordList(models.Model):
    # 单词本
    wordbook = models.ForeignKey(WordBook, on_delete=models.CASCADE)
    # 单词
    word = models.ForeignKey(Dict, on_delete=models.CASCADE)
    # 学习释义
    definition = models.TextField(null=True)

    def __str__(self):
        return '%s' % self.word.text


"""
    这里写死了笔记必须基于某一个单词本中的单词建立。
    如果需要脱离单词本建立笔记，可能需要建立一个特殊的单词本，包含用户见过的或者查询过的单词
"""


# 笔记
class Note(models.Model):
    # 单词表中的单词
    word = models.ForeignKey(WordList, on_delete=models.CASCADE)
    userproperty = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    # 笔记内容
    content = models.TextField(default='')
    # 是否共享
    shared = models.BooleanField(default=True)


# 学习状态
class LearnState(models.Model):
    userproperty = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    word = models.ForeignKey(WordList, on_delete=models.CASCADE)
    # 熟练度
    familiar_level = models.IntegerField(default=0)
    # 太简单标记
    too_simple = models.BooleanField(default=False)
    # 掌握标记
    master = models.BooleanField(default=False)

    class Meta:
        # 一个用户不可能对同一本书的同一个单词有两个学习记录
        unique_together = ('userproperty', 'word')

    def __str__(self):
        ret = 'user=%s,word=%s(%d)' % (
            self.userproperty,
            self.word,
            self.familiar_level,
        )
        if self.master:
            ret += ', master'
        if self.too_simple:
            ret += ', too_simple'
        return ret

    # 我忘了
    def forget(self):
        task = LearnTask.objects.get_or_create(
            userproperty=self.userproperty,
            word=self.word
        )[0]
        task.build_date = datetime.now().date()
        task.remember = False
        task.finished = False
        task.unknown = True
        self.userproperty.get_diary().update()
        self.delete()


class LearnTask(models.Model):
    userproperty = models.ForeignKey(UserProperty, on_delete=models.CASCADE)
    word = models.ForeignKey(WordList, on_delete=models.CASCADE)
    build_date = models.DateField()
    remember = models.BooleanField(auto_created=True, default=False)
    finished = models.BooleanField(auto_created=True, default=False)
    unknown_flag = models.BooleanField(auto_created=True, default=True)
    # 是否是新学习的

    class Meta:
        unique_together = ('userproperty', 'word')

    def get_learn_state(self):
        return LearnState.objects.get_or_create(
            userproperty=self.userproperty,
            word=self.word
        )[0]

    def __str__(self):
        return str(self.get_learn_state())

    # 认识
    def known(self):
        state = self.get_learn_state()
        if state.master:
            return
        if not self.remember:
            self.remember = True
        else:
            self.finished = True
            state.familiar_level += 1
            if state.familiar_level == settings.LEARNING_COUNT:
                state.master = True
            state.save()
        self.save()

    # 不认识
    def unknown(self):
        self.remember = False
        self.finished = False
        self.save()

    # 太简单
    def too_simple(self):
        self.remember = True
        self.finished = True
        self.save()
        state = self.get_learn_state()
        state.too_simple = True
        state.save()
        self.userproperty.get_diary().update()

    # 构造某个用户的学习计划
    @staticmethod
    def generate_task(user, today=datetime.now().date()):
        userp = UserProperty.objects.filter(user=user).first()
        if not userp:
            return
        unknown_words = userp.unknown_words()
        review_words = userp.review_words()
        # 第一次计算
        unknown = min(len(unknown_words), math.ceil(userp.amount * 0.15))
        review = min(userp.amount - unknown, len(review_words))
        # 如果单词总量不够再从不会的里面补充
        if unknown + review < userp.amount:
            unknown = min(userp.amount - review, len(unknown_words))
        # 取样本
        unknown_words = random.sample(unknown_words, unknown)
        review_words = random.sample(review_words, review)

        # 先创建对象然后一次性添加以提高性能
        learn_tasks = []
        for task in unknown_words:
            # 加上判断，防止在用户单词任务生成之前就手动添加过
            if not LearnTask.objects.filter(
                    userproperty=userp, word=task, build_date=today):
                learn_tasks.append(LearnTask(
                    userproperty=userp, word=task, build_date=today, unknown_flag=True))
        for task in review_words:
            # 加上判断，防止在用户单词任务生成之前就手动添加过
            if not LearnTask.objects.filter(
                    userproperty=userp, word=task, build_date=today):
                learn_tasks.append(LearnTask(
                    userproperty=userp, word=task, build_date=today, unknown_flag=False))
        # 乱序
        random.shuffle(learn_tasks)
        return LearnTask.objects.bulk_create(learn_tasks)

    @staticmethod
    def get_user_tasks(user, today=datetime.now().date()):
        userp = UserProperty.objects.filter(user=user).first()
        tasks = userp.learntask_set.all()
        tasks = tasks.filter(build_date__gte=today)
        if not tasks:
            LearnTask.generate_task(user, today=today)
        tasks = userp.learntask_set.all()
        tasks = tasks.filter(build_date=today)
        tasks = tasks.exclude(finished=True)
        return tasks
