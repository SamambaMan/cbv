# coding=utf-8
from django.contrib import admin
from django import forms
from sitecbv.models import *


class BannerRedeDescontoAdmin(admin.ModelAdmin):
    list_display = ['Titulo', 'Ativo']
    list_filter = ('Ativo',)
    search_fields = ('Titulo',)

class RedeDeDescontoAdmin(admin.ModelAdmin):
    list_display = ('Titulo', 'Categoria', 'DataPublicacao', 'Publicar', 'Ativo')
    search_fields = ('Titulo', 'Conteudo',)
    list_filter = ('DataPublicacao', 'Publicar', 'Ativo', 'Categoria')
    fieldsets = (
        ('Geral', {'fields':('Titulo', 'Subtitulo', 'Link', 'Detalhe',
                             'Categoria', 'DataPublicacao', 'Ativo')}),
        ('Imagens', {'fields':('Thumb', 'ImagemCarrossel', 'Topo',)}),
        (u'Publicação', {'fields':('Conteudo', 'Publicar',)}),
    )
    readonly_fields = ('DataPublicacao',)

class ProgramaAdmin(admin.ModelAdmin):
    list_display = ['Titulo', 'Publicar']
    list_filter = ('Publicar',)
    search_fields = ('Titulo', 'Publicar')

class InfosAdicionaisUsuarioAdmin(admin.ModelAdmin):
    empty_value_display = '---'
    list_display = ['get_email', 'get_firstname',
                    'get_active', 'sexo', 'ufed', 'cadastrocompleto']
    search_fields = ('user__email', 'user_first_name',)
    list_filter = ('user__is_active', 'cadastrocompleto')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'E-Mail'
    get_email.admin_order_field = 'user__email'

    def get_firstname(self, obj):
        return obj.user.first_name
    get_firstname.short_description = 'Nome'
    get_firstname.admin_order_field = 'user__first_name'

    def get_active(self, obj):
        return obj.user.is_active
    get_active.short_description = 'Ativo'
    get_active.admin_order_field = 'user__is_active'
    get_active.boolean = True

class ConteudoExclusivoAdmin(admin.ModelAdmin):
    list_display = ('Titulo', 'Categoria', 'DataPublicacao', 'Destaque', 'Publicar',)
    search_fields = ('Titulo', 'Conteudo',)
    list_filter = ('DataPublicacao', 'Destaque', 'Publicar', 'Categoria')
    fieldsets = (
        ('Geral', {'fields':('Titulo', 'Subtitulo', 'Detalhe', 'Categoria', 'DataPublicacao',)}),
        ('Imagens', {'fields':('Thumb', 'ImagemCarrossel', 'Topo',)}),
        (u'Publicação', {'fields':('Conteudo', 'Destaque', 'Publicar',)}),
    )
    readonly_fields = ('DataPublicacao',)

class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('Titulo', 'Categoria', 'DataPublicacao', 'Destaque', 'Publicar', 'Ativo')
    search_fields = ('Titulo', 'Conteudo',)
    list_filter = ('DataPublicacao', 'Destaque', 'Publicar', 'Ativo', 'Categoria')
    fieldsets = (
        ('Geral', {'fields':('Titulo', 'Subtitulo', 'Link', 'Detalhe',
                             'Categoria', 'DataPublicacao', 'Ativo')}),
        ('Imagens', {'fields':('Thumb', 'ImagemCarrossel', 'Topo',)}),
        (u'Publicação', {'fields':('Conteudo', 'Destaque', 'Publicar',)}),
    )
    readonly_fields = ('DataPublicacao',)

class TimeAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Sexo', 'Superliga')
    list_filter = ('Sexo', 'Superliga')
    search_fields = ('Nome',)

class JogadorAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Sexo')
    list_filter = ('Sexo',)
    search_fields = ('Nome',)

admin.site.register(InfosAdicionaisUsuario, InfosAdicionaisUsuarioAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Jogador, JogadorAdmin)
admin.site.register(CategoriaConteudoExclusivo)
admin.site.register(CategoriaExperiencia)
admin.site.register(CategoriaCensoDoVolei)
admin.site.register(CategoriaRedeDeDesconto)
admin.site.register(ConteudoExclusivo, ConteudoExclusivoAdmin)
admin.site.register(Experiencia, ExperienciaAdmin)
admin.site.register(CensoDoVolei)
admin.site.register(RedeDeDesconto, RedeDeDescontoAdmin)
admin.site.register(BannerRedeDesconto, BannerRedeDescontoAdmin)
admin.site.register(BannerCensoDoVolei)
admin.site.register(Programa, ProgramaAdmin)
admin.site.site_header = u'Confederação Brasileira de Volei'

