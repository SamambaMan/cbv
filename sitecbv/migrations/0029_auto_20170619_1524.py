# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitecbv', '0028_auto_20170619_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redededesconto',
            name='Selo',
            field=models.FileField(blank=True, help_text='53x53 px, PNG ou JPG', null=True, upload_to=b''),
        ),
    ]
