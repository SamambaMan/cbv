# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from autoslug import AutoSlugField

# Create your models here.
SEXO_CHOICES = (
    (u'M', u'Masculino'),
    (u'F', u'Feminino'),
    (u'O', u'Outro'),
)

MF_CHOICES = (
    (u'M', u'Masculino'),
    (u'F', u'Feminino'),
)

MODALIDADE_CHOICES = (
    ('VQ', u'Volei de Quadra'),
    ('VP', u'Volei de Praia'),
)

TIPO_DOCUMENTO_CHOICES = (
    ('CPF', u'CPF'),
    ('PAS', u'Passaporte'),
)

SUPERLIGA_CHOICE = (
    ('SA', 'Super Liga A'),
    ('SB', 'Super Liga B'),
)

UF_CHOICES = (
    ('FO','Fora do Brasil'),
    ('AC', u'Acre'),
    ('AL', u'Alagoas'),
    ('AM', u'Amazonas'),
    ('AP', u'Amapá'),
    ('BA', u'Bahia'),
    ('CE', u'Ceará'),
    ('DF', u'Distrito Federal'),
    ('ES', u'Espírito Santo'),
    ('GO', u'Goiás'),
    ('MA', u'Maranhão'),
    ('MG', u'Minas Gerais'),
    ('MS', u'Mato Grosso do Sul'),
    ('MT', u'Mato Grosso'),
    ('PA', u'Pará'),
    ('PB', u'Paraíba'),
    ('PE', u'Pernambuco'),
    ('PI', u'Piauí'),
    ('PR', u'Paraná'),
    ('RJ', u'Rio de Janeiro'),
    ('RN', u'Rio Grande do Norte'),
    ('RO', u'Rondônia'),
    ('RR', u'Roraima'),
    ('RS', u'Rio Grande do Sul'),
    ('SC', u'Santa Catarina'),
    ('SE', u'Sergipe'),
    ('SP', u'São Paulo'),
    ('TO', u'Tocantins'),
)

class InfosAdicionaisUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cadastrocompleto = models.BooleanField(
        default=False, verbose_name='Cadastro Completo')
    cpf = models.CharField(max_length=11, blank=True, null=True, help_text=u"Apenas números")
    tipodocumento = models.CharField(
        max_length=3, default='CPF',
        choices=TIPO_DOCUMENTO_CHOICES, verbose_name='Tipo de Documento')
    ufed = models.CharField(max_length=50, blank=True,
                            null=True, verbose_name="UF", choices=UF_CHOICES)
    sexo = models.CharField(
        max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    celular = models.CharField(max_length=11, blank=True, null=True)
    telefone = models.CharField(max_length=11, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)
    endereco = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'Endereço')
    numero = models.CharField(
        max_length=15, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True,
                            null=True, verbose_name='País')
    modalidade_favorita = models.CharField(
        max_length=2, default='VQ', choices=MODALIDADE_CHOICES)

    jogador_favorito = models.ForeignKey(
    'Jogador', blank=True, null=True, related_name="infos_jogador_favorito")
    jogadora_favorita = models.ForeignKey(
    'Jogador', blank=True, null=True, related_name="infos_jogadora_favorita")
    jogadores_secundario_masculinos = models.ManyToManyField(
    'Jogador', related_name="infos_jogadores_secundario_masculinos", blank=True)
    jogadoras_secundarias_femininas = models.ManyToManyField(
    'Jogador', related_name="infos_jogadoras_secundarias_femininas", blank=True)

    time_favorito_masculino = models.ForeignKey(
    'Time', related_name="infos_time_favorito_masculino", blank=True, null=True)
    time_favorito_feminino = models.ForeignKey(
    'Time', related_name="infos_time_favorito_feminino", blank=True, null=True)
    times_secundarios_masculino = models.ManyToManyField(
    'Time', related_name="infos_times_secundarios_masculino", blank=True)
    times_secundarios_feminino = models.ManyToManyField(
    'Time', related_name="infos_times_secundarios_feminino", blank=True)


class Time(models.Model):
    Nome = models.CharField(max_length=15)
    Sexo = models.CharField(max_length=1, default='M', choices=MF_CHOICES)
    Superliga = models.CharField(max_length=2, default='SA', choices=SUPERLIGA_CHOICE)
    Logo = models.FileField(help_text="300x300 PNG ou JPG")

    def __str__(self):
        if self:
            return self.Nome
        return ""



class Jogador(models.Model):
    Nome = models.CharField(max_length=15)
    Sexo = models.CharField(max_length=1, choices=MF_CHOICES)
    Foto = models.FileField(help_text="300x300 PNG ou JPG")
    
    def __str__(self):
        if self:
            return self.Nome
        return ""

    class Meta:
        verbose_name = u"Jogador"
        verbose_name_plural = u"Jogadores"


class Programa(models.Model):
    Titulo = models.CharField(max_length=50)
    Topo = models.FileField(help_text=u"Alta Resolução, 16x9, PNG ou JPG")
    Conteudo = HTMLField(blank=True, null=True, verbose_name=u'Conteúdo')
    Publicar = models.BooleanField(default=False)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Publicar and Programa.objects.filter(Publicar=True).exclude(id=self.id).count() > 0:
            raise ValidationError(u"Já existe outro programa Publicado")

    def __str__(self):
        if self.Titulo:
            return self.Titulo
        return ""


class Publicavel(models.Model):
    Titulo = models.CharField(max_length=50, verbose_name=u'Título')
    Detalhe = models.CharField(max_length=50, blank=True, null=True)
    Thumb = models.FileField(
        help_text=u"Alta Resolução, 16x9, PNG ou JPG", blank=True, null=True)
    Topo = models.FileField(help_text=u"Alta Resolução, 16x9, PNG ou JPG")
    Conteudo = HTMLField(blank=True, null=True, verbose_name=u'Conteúdo')
    DataPublicacao = models.DateField(
        blank=True, null=True, verbose_name=u'Data de Publicação')
    Publicar = models.BooleanField(default=False)

    def __str__(self):
        if self:
            return self.Titulo
        return ""

    class Meta:
        abstract = True


class Categoria(models.Model):
    Nome = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='Nome', unique=True, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self is not None:
            return self.Nome
        return ""


class CategoriaConteudoExclusivo(Categoria):

    class Meta:
        verbose_name = u"Categoria Conteúdo Exclusivo"
        verbose_name_plural = u"Categorias Conteúdo Exclusivo"


class CategoriaExperiencia(Categoria):

    class Meta:
        verbose_name = u"Categoria Experiência"
        verbose_name_plural = u"Categorias Experiência"


class CategoriaCensoDoVolei(Categoria):

    class Meta:
        verbose_name = u"Categoria Censo do Volei"
        verbose_name_plural = u"Categorias Censo do Volei"


class CategoriaRedeDeDesconto(Categoria):

    class Meta:
        verbose_name = "Categoria Rede de Desconto"
        verbose_name_plural = "Categorias Rede de Desconto"


class ConteudoExclusivo(Publicavel):
    Destaque = models.BooleanField(default=False)
    ImagemCarrossel = models.FileField(
        blank=True, null=True, help_text=u"Alta Resolução, 16x9, PNG ou JPG",
        verbose_name='Imagem Carrossel')
    Categoria = models.ForeignKey('CategoriaConteudoExclusivo')

    class Meta:
        verbose_name = u"Conteúdo Exclusivo"
        verbose_name_plural = u"Conteúdos Exclusivos"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Publicar:
            if not self.Titulo or not self.Detalhe or not self.Conteudo or \
                    not self.Thumb or not self.ImagemCarrossel:
                raise ValidationError(u"""Para Publicar é necessário preencher os campos:
                Título,
                Detalhe,
                Conteúdo,
                Imagem de Carrossel,
                Imagem de Thumb,
                Imagem de Topo,
                Conteúdo""")

    def save(self, *args, **kwargs):
        from datetime import datetime
        if self.Publicar:
            if self.id:
                conteudoanterior = ConteudoExclusivo.objects.get(id=self.id)
                if not conteudoanterior.Publicar:
                    self.DataPublicacao = datetime.now()
            self.DataPublicacao = datetime.now()

        super(ConteudoExclusivo, self).save(*args, **kwargs)


class Experiencia(Publicavel):
    Categoria = models.ForeignKey('CategoriaExperiencia')
    ImagemCarrossel = models.FileField(
        blank=True, null=True, help_text="Alta Resolução, 16x9, PNG ou JPG")
    Destaque = models.BooleanField(default=False)
    Link = models.CharField(max_length=1000)
    Ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"Experiência"
        verbose_name_plural = u"Experiências"


class CensoDoVolei(Publicavel):
    Categoria = models.ForeignKey('CategoriaCensoDoVolei')
    ImagemCarrossel = models.FileField(
        blank=True, null=True, help_text="Alta Resolução, 16x9, PNG ou JPG")
    Link = models.CharField(max_length=1000)
    Ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"Censo do Volei"
        verbose_name_plural = u"Censos do Volei"


class RedeDeDesconto(Publicavel):
    Categoria = models.ForeignKey('CategoriaRedeDeDesconto')
    ImagemCarrossel = models.FileField(
        blank=True, null=True, help_text="Alta Resolução, 16x9, PNG ou JPG")
    Link = models.CharField(max_length=1000)
    Ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"Rede de Desconto"
        verbose_name_plural = u"Redes de Desconto"


class BannerRedeDesconto(models.Model):
    Titulo = models.CharField(max_length=100, verbose_name="Título")
    Imagem = models.FileField(help_text="Alta Resolução, 16x9, PNG ou JPG")
    Ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Banner Rede de Desconto"
        verbose_name_plural = "Banneres Rede de Desconto"


class BannerCensoDoVolei(models.Model):
    Titulo = models.CharField(max_length=100)
    Imagem = models.FileField(help_text="Alta Resolução, 16x9, PNG ou JPG")
    Ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Banner Censo do Volei"
        verbose_name_plural = "Banneres Censo do Volei"
