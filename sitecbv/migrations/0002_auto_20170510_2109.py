# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 21:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitecbv', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bannercensodovolei',
            options={'verbose_name': 'Banner Censo do Volei', 'verbose_name_plural': 'Banneres Censo do Volei'},
        ),
        migrations.AlterModelOptions(
            name='bannerrededesconto',
            options={'verbose_name': 'Banner Rede de Desconto', 'verbose_name_plural': 'Banneres Rede de Desconto'},
        ),
        migrations.AlterModelOptions(
            name='categoriacensodovolei',
            options={'verbose_name': 'Categoria Censo do Volei', 'verbose_name_plural': 'Categorias Censo do Volei'},
        ),
        migrations.AlterModelOptions(
            name='categoriaconteudoexclusivo',
            options={'verbose_name': 'Categoria Conte\xfado Exclusivo', 'verbose_name_plural': 'Categorias Conte\xfado Exclusivo'},
        ),
        migrations.AlterModelOptions(
            name='categoriaexperiencia',
            options={'verbose_name': 'Categoria Experi\xeancia', 'verbose_name_plural': 'Categorias Experi\xeancia'},
        ),
        migrations.AlterModelOptions(
            name='categoriaredededesconto',
            options={'verbose_name': 'Categoria Rede de Desconto', 'verbose_name_plural': 'Categorias Rede de Desconto'},
        ),
        migrations.AlterModelOptions(
            name='censodovolei',
            options={'verbose_name': 'Censo do Volei', 'verbose_name_plural': 'Censos do Volei'},
        ),
        migrations.AlterModelOptions(
            name='conteudoexclusivo',
            options={'verbose_name': 'Conte\xfado Exclusivo', 'verbose_name_plural': 'Conte\xfados Exclusivos'},
        ),
        migrations.AlterModelOptions(
            name='experiencia',
            options={'verbose_name': 'Experi\xeancia', 'verbose_name_plural': 'Experi\xeancias'},
        ),
        migrations.AlterModelOptions(
            name='jogador',
            options={'verbose_name': 'Jogador', 'verbose_name_plural': 'Jogadores'},
        ),
        migrations.AlterModelOptions(
            name='redededesconto',
            options={'verbose_name': 'Rede de Desconto', 'verbose_name_plural': 'Redes de Desconto'},
        ),
        migrations.AlterField(
            model_name='bannercensodovolei',
            name='Imagem',
            field=models.FileField(help_text='Alta Resolu\xe7\xe3o, 16x9, PNG ou JPG', upload_to=b''),
        ),
        migrations.AlterField(
            model_name='bannerrededesconto',
            name='Imagem',
            field=models.FileField(help_text='Alta Resolu\xe7\xe3o, 16x9, PNG ou JPG', upload_to=b''),
        ),
        migrations.AlterField(
            model_name='bannerrededesconto',
            name='Titulo',
            field=models.CharField(max_length=100, verbose_name='T\xedtulo'),
        ),
        migrations.AlterField(
            model_name='infosadicionaisusuario',
            name='jogadoras_secundarias_femininas',
            field=models.ManyToManyField(blank=True, related_name='infos_jogadoras_secundarias_femininas', to='sitecbv.Jogador'),
        ),
        migrations.AlterField(
            model_name='infosadicionaisusuario',
            name='jogadores_secundario_masculinos',
            field=models.ManyToManyField(blank=True, related_name='infos_jogadores_secundario_masculinos', to='sitecbv.Jogador'),
        ),
        migrations.AlterField(
            model_name='infosadicionaisusuario',
            name='time_favorito_feminino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='infos_time_favorito_feminino', to='sitecbv.Time'),
        ),
        migrations.AlterField(
            model_name='infosadicionaisusuario',
            name='time_favorito_masculino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='infos_time_favorito_masculino', to='sitecbv.Time'),
        ),
        migrations.AlterField(
            model_name='infosadicionaisusuario',
            name='times_secundarios_feminino',
            field=models.ManyToManyField(blank=True, related_name='infos_times_secundarios_feminino', to='sitecbv.Time'),
        ),
        migrations.AlterField(
            model_name='infosadicionaisusuario',
            name='times_secundarios_masculino',
            field=models.ManyToManyField(blank=True, related_name='infos_times_secundarios_masculino', to='sitecbv.Time'),
        ),
        migrations.AlterField(
            model_name='infosadicionaisusuario',
            name='ufed',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='UF'),
        ),
    ]