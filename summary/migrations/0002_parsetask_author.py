# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-17 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parsetask',
            name='author',
            field=models.CharField(db_index=True, default='__nobody__', max_length=32),
        ),
    ]
