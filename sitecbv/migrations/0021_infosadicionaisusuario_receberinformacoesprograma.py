# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitecbv', '0020_auto_20170607_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='infosadicionaisusuario',
            name='receberinformacoesprograma',
            field=models.BooleanField(default=True),
        ),
    ]
