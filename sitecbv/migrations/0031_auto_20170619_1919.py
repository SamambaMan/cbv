# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitecbv', '0030_auto_20170619_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogador',
            name='Foto',
            field=models.FileField(blank=True, help_text='300x300 PNG ou JPG', null=True, upload_to=b''),
        ),
    ]
