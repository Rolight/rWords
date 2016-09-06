# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-06 07:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rwords', '0005_auto_20160906_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='learning_wordbook',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rwords.WordBook'),
        ),
    ]
