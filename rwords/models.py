from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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
    pub_date = models.DateField(auto_now_add=True, editable=False)
    update_date = models.DateField(auto_now=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(null=False, default='unnamed wordbook')
    words = models.ManyToManyField(Dict, through='WordList')

    def __str__(self):
        return '%s from %s' % (self.name, self.author.username)


class WordList(models.Model):
    wordbook = models.ForeignKey(WordBook, on_delete=models.CASCADE)
    word = models.ForeignKey(Dict, on_delete=models.CASCADE)
    definition = models.TextField(null=True)

    def __str__(self):
        return '%s: %s' % (self.word.text, self.definition)

