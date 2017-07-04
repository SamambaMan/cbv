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
    ('AM', u'Ambos'),
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
    ('', '--------------'),
    ('FO', u'Fora do Brasil'),
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
    nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(
        max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'Endereço')
    numero = models.CharField(
        max_length=15, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True,
                            null=True, verbose_name='País')
    legado = models.BooleanField(default=False)

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

    receberinformacoesprograma = models.BooleanField(default=True)

    def clean(self):
        from django.forms import ValidationError
        from .snipets import validate_CPF
        if self.ufed != "FO":
            validate_CPF(self.cpf)

        if self.id and \
            InfosAdicionaisUsuario.objects.filter(cpf=self.cpf).exclude(id=self.id).count() > 0:
            raise ValidationError(u"CPF informado já foi cadastrado por outro usuário")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(InfosAdicionaisUsuario, self).save(*args, **kwargs)



class Time(models.Model):
    Nome = models.CharField(max_length=35)
    Sexo = models.CharField(max_length=1, default='M', choices=MF_CHOICES)
    Superliga = models.CharField(max_length=2, default='SA', choices=SUPERLIGA_CHOICE)
    Logo = models.FileField(help_text="55x45px PNG ou JPG")
    Link = models.CharField(max_length=1000, default="#")
    Nenhum = models.BooleanField(default=False)

    def __str__(self):
        if self:
            return self.Nome
        return ""



class Jogador(models.Model):
    Nome = models.CharField(max_length=35)
    Sexo = models.CharField(max_length=1, choices=MF_CHOICES)
    Foto = models.FileField(help_text="300x300 PNG ou JPG", null=True, blank=True,)
    Nenhum = models.BooleanField(default=False)

    def __str__(self):
        if self:
            return self.Nome
        return ""

    class Meta:
        verbose_name = u"Jogador"
        verbose_name_plural = u"Jogadores"


class Programa(models.Model):
    Titulo = models.CharField(max_length=50)
    Subtitulo = models.CharField(max_length=100, default="")
    Topo = models.FileField(help_text=u"908x302 px, PNG ou JPG")
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
    Subtitulo = models.CharField(max_length=140, verbose_name=u'Subtítulo', null=True, blank=True)
    Detalhe = models.CharField(max_length=140, blank=True, null=True)
    Thumb = models.FileField(
        help_text=u"170x200 px, PNG ou JPG", blank=True, null=True)
    Topo = models.FileField(help_text=u"945 x 365 px, PNG ou JPG", blank=True, null=True)
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

    def save(self, *args, **kwargs):
        from datetime import datetime
        if self.Publicar:
            if self.id:
                conteudoanterior = self.__class__.objects.get(id=self.id)
                if not conteudoanterior.Publicar:
                    self.DataPublicacao = datetime.now()
            self.DataPublicacao = datetime.now()

        super(Publicavel, self).save(*args, **kwargs)


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
        blank=True, null=True, help_text=u"912x500 px, PNG ou JPG",
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


class Experiencia(Publicavel):
    Categoria = models.ForeignKey('CategoriaExperiencia')
    ImagemCarrossel = models.FileField(verbose_name=u'Imagem Carrossel',
        blank=True, null=True, help_text="912x500 px, PNG ou JPG")
    Destaque = models.BooleanField(default=False)
    Link = models.CharField(max_length=1000, verbose_name=u'Link Externo')
    Ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"Experiência"
        verbose_name_plural = u"Experiências"

class BannerExperiencia(models.Model):
    Titulo = models.CharField(max_length=50)
    Subtitulo = models.CharField(max_length=100, null=True, blank=True,)
    Ativo = models.BooleanField()

    class Meta:
        verbose_name = u"Banner Experiência"
        verbose_name_plural = u"Banneres Experiências"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Ativo and BannerExperiencia.objects.filter(Ativo=True).exclude(id=self.id).count() > 0:
            raise ValidationError(u"Já existe outro Banner Ativo")

    def __str__(self):
        if self.Titulo:
            return self.Titulo
        return ""

class BannerConteudoExclusivo(models.Model):
    Titulo = models.CharField(max_length=50)
    Subtitulo = models.CharField(max_length=100, null=True, blank=True,)
    Ativo = models.BooleanField()

    class Meta:
        verbose_name = u"Banner Conteúdo Exclusivo"
        verbose_name_plural = u"Banneres Conteúdo Exclusivo"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Ativo and BannerConteudoExclusivo.objects.filter(Ativo=True).exclude(id=self.id).count() > 0:
            raise ValidationError(u"Já existe outro Banner Ativo")

    def __str__(self):
        if self.Titulo:
            return self.Titulo
        return ""

class CensoDoVolei(Publicavel):
    Categoria = models.ForeignKey('CategoriaCensoDoVolei')
    ImagemCarrossel = models.FileField(
        blank=True, null=True, help_text="912x500 px, PNG ou JPG")
    Link = models.CharField(max_length=1000)
    Destaque = models.BooleanField(default=False)
    Ativo = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(CensoDoVolei, self).__init__(*args, **kwargs)
        self._meta.get_field('Thumb').help_text = "230x200 px, PNG ou JPG"

    class Meta:
        verbose_name = u"Censo do Volei"
        verbose_name_plural = u"Censos do Volei"


class RedeDeDesconto(Publicavel):
    Categoria = models.ForeignKey('CategoriaRedeDeDesconto')
    ImagemCarrossel = models.FileField(
        blank=True, null=True, help_text="912x500 px, PNG ou JPG")
    Selo = models.FileField(blank=True, null=True, help_text="53x53 px, PNG ou JPG")
    Link = models.CharField(max_length=1000)
    Ativo = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(RedeDeDesconto, self).__init__(*args, **kwargs)
        self._meta.get_field('Thumb').help_text = "257x200 px, PNG ou JPG"

    class Meta:
        verbose_name = u"Rede de Desconto"
        verbose_name_plural = u"Redes de Desconto"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Publicar and (\
                    not self.Titulo\
                    or not self.Subtitulo\
                    or not self.Link\
                    or not self.Detalhe\
                    or not self.Categoria\
                    or not self.Thumb\
                    or not self.Selo):
            raise ValidationError(u"Para publicar um conteúdo todos os campos são obrigatórios")


class BannerHome(models.Model):
    Titulo = models.CharField(max_length=100, verbose_name=u"Título")
    Subtitulo = models.CharField(max_length=100, verbose_name=u"Subtítulo", null=True, blank=True, default="")
    ImagemCarrossel = models.FileField(
        help_text=u"912x500 px, PNG ou JPG",
        verbose_name='Imagem Carrossel')
    Link = models.CharField(max_length=1000, default="#", help_text="Informe link completo como 'http://eusoudovolei.com.br/'")
    Ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Banner Home"
        verbose_name_plural = "Banneres Home"

    def __str__(self):
        if self.Titulo:
            return self.Titulo
        return ""

class BannerRedeDesconto(models.Model):
    Titulo = models.CharField(max_length=100, verbose_name=u"Título")
    Subtitulo = models.CharField(max_length=100, verbose_name=u"Subtítulo", null=True, blank=True, default="")
    Imagem = models.FileField(blank=True, null=True, help_text="908x302 px, PNG ou JPG")
    Ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Banner Rede de Desconto"
        verbose_name_plural = "Banneres Rede de Desconto"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Ativo and BannerRedeDesconto.objects.filter(Ativo=True).exclude(id=self.id).count() > 0:
            raise ValidationError(u"Já existe outro Banner Ativo")

    def __str__(self):
        if self.Titulo:
            return self.Titulo
        return ""


class BannerCensoDoVolei(models.Model):
    Titulo = models.CharField(max_length=100)
    Subtitulo = models.CharField(max_length=100, blank=True, null=True)
    Ativo = models.BooleanField(default=False)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Ativo and BannerCensoDoVolei.objects.filter(Ativo=True).exclude(id=self.id).count() > 0:
            raise ValidationError(u"Já existe outro Banner Ativo")

    def __str__(self):
        if self.Titulo:
            return self.Titulo
        return ""


    class Meta:
        verbose_name = "Banner Censo do Volei"
        verbose_name_plural = "Banneres Censo do Volei"
