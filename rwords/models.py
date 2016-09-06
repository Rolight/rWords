from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class authUser(User):
    # 正在学习的单词书
    learning_wordbook = models.ForeignKey('WordBook', on_delete=None, null=True, default=None)
    # 每日学习量
    amount = models.IntegerField(null=False, default=50)
    # 笔记
    notes = models.ManyToManyField('WordList', related_name='note_users', through='Note')
    # 学习记录
    states = models.ManyToManyField('WordList', related_name='learn_users', through='LearnState')

# 词库
class Dict(models.Model):
    text = models.TextField(null=False, unique=True, default='')

    def __str__(self):
        return self.text


# 例句
class Example(models.Model):
    word = models.ForeignKey(Dict, on_delete=models.CASCADE)
    text = models.TextField(null=False, default='')


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
    author = models.ForeignKey(authUser, on_delete=models.CASCADE)
    # 单词书名称
    name = models.TextField(null=False, default='unnamed wordbook')
    # 单词表
    words = models.ManyToManyField(Dict, through='WordList')

    def __str__(self):
        return '%s from %s' % (self.name, self.author.username)


class WordList(models.Model):
    # 单词本
    wordbook = models.ForeignKey(WordBook, on_delete=models.CASCADE)
    # 单词
    word = models.ForeignKey(Dict, on_delete=models.CASCADE)
    # 学习释义
    definition = models.TextField(null=True)

    def __str__(self):
        return '%s: %s' % (self.word.text, self.definition)


"""
    这里写死了笔记必须基于某一个单词本中的单词建立。
    如果需要脱离单词本建立笔记，可能需要建立一个特殊的单词本，包含用户见过的或者查询过的单词
"""
# 笔记
class Note(models.Model):
    # 单词表中的单词
    word = models.ForeignKey(WordList, on_delete=models.CASCADE)
    user = models.ForeignKey(authUser, on_delete=models.CASCADE)
    # 笔记内容
    content = models.TextField(default='')
    # 是否共享
    shared = models.BooleanField(default=True)

#学习状态
class LearnState(models.Model):
    user = models.ForeignKey(authUser, on_delete=models.CASCADE)
    word = models.ForeignKey(WordList, on_delete=models.CASCADE)
    # 熟练度
    familiar_level = models.IntegerField(default=0)
    # 太简单标记
    too_simple = models.BooleanField(default=False)
    # 掌握标记
    learned = models.BooleanField(default=False)

    class Meta:
        # 一个用户不可能对同一本书的同一个单词有两个学习记录
        unique_together = ('user', 'word')
