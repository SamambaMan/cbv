# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitecbv', '0014_auto_20170601_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='Link',
            field=models.CharField(default='#', max_length=1000),
        ),
    ]
