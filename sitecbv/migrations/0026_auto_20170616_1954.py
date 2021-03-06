# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitecbv', '0025_auto_20170613_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='censodovolei',
            name='Topo',
            field=models.FileField(blank=True, help_text='945 x 365 px, PNG ou JPG', null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='conteudoexclusivo',
            name='Topo',
            field=models.FileField(blank=True, help_text='945 x 365 px, PNG ou JPG', null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='experiencia',
            name='Topo',
            field=models.FileField(blank=True, help_text='945 x 365 px, PNG ou JPG', null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='redededesconto',
            name='Topo',
            field=models.FileField(blank=True, help_text='945 x 365 px, PNG ou JPG', null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='time',
            name='Logo',
            field=models.FileField(help_text='55x45px PNG ou JPG', upload_to=b''),
        ),
    ]
