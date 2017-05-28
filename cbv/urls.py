"""cbv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout

from sitecbv.views import index, cadastrousuariobasico,\
                          cadastrarusuariobasico, programa, conteudoexclusivo,\
                          categoriaconteudoexclusivo, maisconteudoexclusivo,\
                          detalheconteudoexclusivo, cadastrocomplementar, efetuarlogin,\
                          experiencias, maisexperiencias, detalheexperiencias, rededescontos,\
                          complementarendereco, detalherededescontos, faleconosco


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', index),
    # Programa
    url(r'^programa/', programa),
    # Conteudo Exclusivo
    url(r'^conteudoexclusivo/$', conteudoexclusivo),
    url(r'^conteudoexclusivo/mais/$', maisconteudoexclusivo),
    url(r'^conteudoexclusivo/listas/(?P<categoria>[\w|-]+)/$$', categoriaconteudoexclusivo),
    url(r'^conteudoexclusivo/listas/(?P<categoria>[\w|-]+)/(?P<id>\d+)/$',
        detalheconteudoexclusivo),
    #Experiencias
    url(r'^experiencias/$', experiencias),
    url(r'^experiencias/mais/$', maisexperiencias),
    url(r'^experiencias/listas/(?P<categoria>[\w|-]+)/(?P<id>\d+)/$', detalheexperiencias),
    url(r'^complementarendereco/$', complementarendereco),

    #Experiencias
    url(r'^rededescontos/$', rededescontos),
    url(r'^rededescontos/listas/(?P<categoria>[\w|-]+)/(?P<id>\d+)/$', detalherededescontos),

    # Cadastro de Usuario
    url(r'^cadastrarusuariobasico/', cadastrarusuariobasico),
    url(r'^cadastrousuariobasico/', cadastrousuariobasico),
    url(r'^cadastrocomplementar/$', cadastrocomplementar),
    # Login
    url(r'^login/$', efetuarlogin),
    url(r'^logout/$', logout, {'next_page': '/'}),

    #Fale Conosco
    url(r'^faleconosco/$', faleconosco),



    url(r'^tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
