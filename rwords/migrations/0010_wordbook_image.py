# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-07 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rwords', '0009_auto_20160907_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordbook',
            name='image',
            field=models.TextField(default='', null=True),
        ),
    ]
