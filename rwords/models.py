from django.db import models

# Create your models here.


class Dict(models.Model):
    text = models.TextField(
        null=False,
        verbose_name='单词',
        unique=True,
        default=''
    )

    def __str__(self):
        return text

class Example(models.Model):
    word = models.ForeignKey(Dict, on_delete=models.CASCADE)
    text = models.TextField(null=False, default='')

class Synonym(models.Model):
    word = models.ForeignKey(Dict, on_delete=models.CASCADE)
    text = models.TextField(null=False, default='')
