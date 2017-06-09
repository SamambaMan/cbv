from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .decorators import obrigar_cadastro_complementar


def torcidometro_times():
    from django.db.models import F, Count
    from .models import Time

    todos_times = Time.objects.filter()

    somatimes = todos_times.annotate(qtd_masculino=Count('infos_time_favorito_masculino'))
    somatimes = somatimes.annotate(qtd_feminino=Count('infos_time_favorito_feminino'))
    somatimes = somatimes.annotate(soma=F('qtd_masculino') + F('qtd_feminino')).order_by('-soma')

    valortotal = 0
    for atual in somatimes.values_list('soma'):
        valortotal = valortotal + atual[0]

    if valortotal != 0:
        somatimes = somatimes.annotate(percentual=(F('soma') * 100)/valortotal)
    else:
        somatimes = somatimes.annotate(percentual=F('soma'))

    return somatimes[:10]

def torcidometro_modalidades():
    from .models import InfosAdicionaisUsuario
    qtd_quadra = InfosAdicionaisUsuario.objects.filter(modalidade_favorita='VQ').count()
    qtd_praia = InfosAdicionaisUsuario.objects.filter(modalidade_favorita='VP').count()
    qtd_ambos = InfosAdicionaisUsuario.objects.filter(modalidade_favorita='AM').count()
    total = qtd_quadra + qtd_praia + qtd_ambos

    qtd_quadra = qtd_quadra * 100 / total
    qtd_praia = qtd_praia * 100 / total
    qtd_ambos = qtd_ambos * 100 / total

    return {'quadra': qtd_quadra, 'praia': qtd_praia, 'ambos': qtd_ambos}

@obrigar_cadastro_complementar
def index(request):
    from .forms import CadastroUsuarioBasicoForm, LoginForm
    conteudos_carrossel = conteudospublicados().filter(
        Destaque=True)[:5]


    return render(request, 'cbv/index.html',
                  {'formcadastrobasico': CadastroUsuarioBasicoForm(),
                   'formlogin': LoginForm(),
                   'conteudos_carrossel': conteudos_carrossel,
                   'torc_mod': torcidometro_modalidades(),
                   'torc_times': torcidometro_times()})


def cadastrousuariobasico(request):
    from .forms import CadastroUsuarioBasicoForm, LoginForm
    return render(request, 'cbv/cadastrobasico.html',
                  {'formcadastrobasico': CadastroUsuarioBasicoForm(),
                   'formlogin': LoginForm()})


def efetuarlogin(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import login
    from django.shortcuts import redirect
    from .forms import LoginForm, CadastroUsuarioBasicoForm

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = User.objects.get(email=form.cleaned_data['email'])

            login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('/')


        return render(request, 'cbv/cadastrobasico.html',
                      {'formcadastrobasico': CadastroUsuarioBasicoForm(),
                       'formlogin': form})

    return render(request, 'cbv/cadastrobasico.html',
                  {'formcadastrobasico': CadastroUsuarioBasicoForm(),
                   'formlogin': LoginForm()})



def cadastrarusuariobasico(request):
    from allauth.account.adapter import DefaultAccountAdapter
    from django.db import transaction
    from django.contrib.auth import login
    from django.shortcuts import redirect
    from django.core.exceptions import ValidationError
    from .forms import CadastroUsuarioBasicoForm, LoginForm

    if request.method == 'POST':
        form = CadastroUsuarioBasicoForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    adapt = DefaultAccountAdapter()
                    novo = adapt.new_user(request)

                    novo.first_name = form.cleaned_data['firstname']
                    novo.email = form.email = form.cleaned_data['email']
                    novo.set_password(form.cleaned_data['password'])
                    adapt.populate_username(request, novo)

                    novo.save()

                    informacoes = novo.infosadicionaisusuario
                    informacoes.user = novo
                    informacoes.ufed = form.cleaned_data['unidadefederativa']
                    informacoes.cpf = form.cleaned_data['cpfpassaporte']


                    informacoes.save()
            except ValidationError as error:
                return render(request,
                              'cbv/cadastrobasico.html',
                              {'formcadastrobasico': form,
                               'formlogin':LoginForm(),
                               'errors':error})

            login(request, novo, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('/cadastrocomplementar/')

        return render(request,
                      'cbv/cadastrobasico.html',
                      {'formcadastrobasico': form, 'formlogin':LoginForm()})

    else:
        return HttpResponseForbidden()

@obrigar_cadastro_complementar
def programa(request):
    from .models import Programa
    programas = Programa.objects.filter(Publicar=True)

    prg = None
    if programas.count() > 0:
        prg = programas[0]

    return render(request, 'cbv/programa.html', {'programa': prg})


def conteudospublicados():
    from .models import ConteudoExclusivo
    return ConteudoExclusivo.objects.filter(Publicar=True).order_by('-DataPublicacao')

@obrigar_cadastro_complementar
def conteudoexclusivo(request):
    from .models import ConteudoExclusivo, CategoriaConteudoExclusivo, BannerConteudoExclusivo
    from .forms import FormBuscaSimples

    conteudos_exibir = []
    for categoria in CategoriaConteudoExclusivo.objects.all():
        conteudos = conteudospublicados().filter(
            Destaque=True, Categoria=categoria).order_by('-DataPublicacao')
        if conteudos.count() > 0:
            conteudos_exibir.append(conteudos[0])


    conteudos_carrossel = conteudospublicados().filter(
        Destaque=True).order_by('-DataPublicacao')[:5]

    bannerconteudo = BannerConteudoExclusivo.objects.filter(Ativo=True).first()


    return render(request, 'cbv/conteudoexclusivo/conteudoexclusivo.html',
                  {'conteudos_exibir': conteudos_exibir,
                   'conteudos_carrossel': conteudos_carrossel, 
                   'mostrarcompleto': True,
                   'banner': bannerconteudo,
                   'form': FormBuscaSimples()})

def buscarpublicacao(listabasica, termos):
    from django.db.models import Q
    return listabasica.filter(Q(Titulo__icontains=termos)|Q(Conteudo__icontains=termos)|Q(Detalhe__icontains=termos))

@obrigar_cadastro_complementar
def categoriaconteudoexclusivo(request, categoria):
    from .models import CategoriaConteudoExclusivo
    from .forms import FormBuscaSimples

    acategoria = CategoriaConteudoExclusivo.objects.get(slug=categoria)

    conteudos = conteudospublicados().filter(Categoria__slug=categoria)
    form = FormBuscaSimples()
    if request.method == 'POST':
        form = FormBuscaSimples(request.POST)
        form.is_valid()

        termos = form.cleaned_data['busca']

        conteudos = buscarpublicacao(conteudos, termos)

    return render(request,
                  'cbv/conteudoexclusivo/catconteudoexclusivo.html',
                  {'conteudos':conteudos, 'categoria':acategoria, 'form':form})

@obrigar_cadastro_complementar
def maisconteudoexclusivo(request):
    from .forms import FormBuscaSimples

    form = FormBuscaSimples()

    conteudos = conteudospublicados()

    if request.method == 'POST':
        form = FormBuscaSimples(request.POST)
        form.is_valid()

        termos = form.cleaned_data['busca']

        conteudos = buscarpublicacao(conteudos, termos)

    return render(request,
                  'cbv/conteudoexclusivo/catconteudoexclusivo.html',
                  {'conteudos':conteudos, 'form':form})

@obrigar_cadastro_complementar
def detalheconteudoexclusivo(request, categoria, id):
    from .forms import CadastroUsuarioBasicoForm, LoginForm
    conteudos = conteudospublicados()

    conteudo = conteudos.get(Categoria__slug=categoria, id=id)

    return render(request,
                  'cbv/conteudoexclusivo/detalheconteudoexclusivo.html',
                  {'conteudo':conteudo,
                   'formcadastrobasico': CadastroUsuarioBasicoForm(),
                   'formlogin': LoginForm()})

def obterformcomplementar(request):
    from .forms import CadastroComplementar
    from .models import Time, Jogador

    usuario = request.user

    jogadores = Jogador.objects.filter(Sexo='M')
    jogadoras = Jogador.objects.filter(Sexo='F')
    timesm = Time.objects.filter(Sexo='M')
    timesf = Time.objects.filter(Sexo='F')

    if request.method == 'POST':
        formulario = CadastroComplementar(request.POST, instance=usuario.infosadicionaisusuario)
    else:
        formulario = CadastroComplementar(instance=usuario.infosadicionaisusuario)

    formulario.fields["jogador_favorito"].queryset = jogadores
    formulario.fields["jogadora_favorita"].queryset = jogadoras
    formulario.fields["jogadores_secundario_masculinos"].queryset = jogadores
    formulario.fields["jogadoras_secundarias_femininas"].queryset = jogadoras

    formulario.fields["time_favorito_masculino"].queryset = timesm
    formulario.fields["time_favorito_feminino"].queryset = timesf
    formulario.fields["times_secundarios_masculino"].queryset = timesm
    formulario.fields["times_secundarios_feminino"].queryset = timesf

    return formulario

def enviaremailcadastrocomplementar(request):
    from django.template.loader import get_template
    from django.core.mail import EmailMultiAlternatives
    from django.conf import settings

    corpo = {'nome': request.user.first_name,
             'endereco': settings.ENDERECO}

    html = get_template('cbv/cadastrousuario/email_cadcomplementar.html')
    text = get_template('cbv/cadastrousuario/email_cadcomplementar.txt')

    subject, from_email, to = 'Bem Vindo CBV', settings.EMAIL_HOST_USER, [request.user.email]
    html_content = html.render(corpo)
    text_content = text.render(corpo)

    msg = EmailMultiAlternatives(subject,
                                 text_content,
                                 from_email=from_email,
                                 to=to)

    msg.attach_alternative(html_content, "text/html")

    msg.send()


@login_required
def cadastrocomplementar(request):
    from .models import InfosAdicionaisUsuario
    from django.contrib.auth import login
    from django.contrib.auth.models import User

    formulario = obterformcomplementar(request)

    if request.method == 'POST':
        if formulario.is_valid():

            antigo = InfosAdicionaisUsuario.objects.get(id=formulario.instance.id).cadastrocompleto

            informacoes = formulario.save()

            if formulario.cleaned_data['senhanova']:
                usuario = User.objects.get(id=request.user.id)
                usuario.set_password(formulario.cleaned_data['senhanova'])
                usuario.save()
                login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')

            if not antigo:
                informacoes.cadastrocompleto = True
                informacoes.save()
                enviaremailcadastrocomplementar(request)

            return render(request, 'cbv/cadastrousuario/cadastrocompleto.html')

    return render(request,
                  'cbv/cadastrousuario/cadastrocomplementar.html',
                  {'formulario':formulario})



############ Experiencias ##############

def experienciaspublicadas():
    from .models import Experiencia
    return Experiencia.objects.filter(Publicar=True).order_by('-DataPublicacao')

@obrigar_cadastro_complementar
def experiencias(request):
    from .models import BannerExperiencia
    from .forms import FormBuscaSimples

    experiencias_exibir = experienciaspublicadas()[:6]

    bannerexperiencia = BannerExperiencia.objects.filter(Ativo=True).first()

    form = FormBuscaSimples()
    if request.method == 'POST':
        form = FormBuscaSimples(request.POST)
        form.is_valid()

        termos = form.cleaned_data['busca']

        experiencias_exibir = buscarpublicacao(experiencias_exibir, termos)

    experiencias_carrossel = experienciaspublicadas().filter(Destaque=True)[:5]

    return render(request, 'cbv/experiencias/experiencias.html',
                  {'conteudos_exibir': experiencias_exibir,
                   'conteudos_carrossel': experiencias_carrossel,
                   'mostrarcompleto': True,
                   'banner': bannerexperiencia,
                   'form': form})

@obrigar_cadastro_complementar
def maisexperiencias(request):
    from .forms import FormBuscaSimples

    form = FormBuscaSimples()

    conteudos = experienciaspublicadas()

    if request.method == 'POST':
        form = FormBuscaSimples(request.POST)
        form.is_valid()

        termos = form.cleaned_data['busca']

        conteudos = buscarpublicacao(conteudos, termos)

    return render(request,
                  'cbv/experiencias/catexperiencias.html',
                  {'conteudos':conteudos, 'form':form})

@obrigar_cadastro_complementar
def detalheexperiencias(request, categoria, id):
    from .forms import CadastroUsuarioBasicoForm, LoginForm
    conteudos = experienciaspublicadas()

    conteudo = conteudos.get(Categoria__slug=categoria, id=id)

    return render(request,
                  'cbv/experiencias/detalheexperiencias.html',
                  {'conteudo':conteudo,
                   'formcadastrobasico': CadastroUsuarioBasicoForm(),
                   'formlogin': LoginForm(),
                   'enderecocompleto': estariaenderecocompleto(request)})

def estariaenderecocompleto(request):
    return request.user.is_authenticated \
        and request.user.infosadicionaisusuario.cep\
        and request.user.infosadicionaisusuario.endereco\
        and request.user.infosadicionaisusuario.numero\
        and request.user.infosadicionaisusuario.bairro\
        and request.user.infosadicionaisusuario.cidade\
        and request.user.infosadicionaisusuario.pais\
        and request.user.infosadicionaisusuario.ufed

def obterformcomplementarendereco(request):
    from .forms import FormComplementarEndereco

    usuario = request.user

    if request.method == 'POST':
        formulario = FormComplementarEndereco(request.POST, instance=usuario.infosadicionaisusuario)
    else:
        formulario = FormComplementarEndereco(instance=usuario.infosadicionaisusuario)

    return formulario

def complementarendereco(request):
    formulario = obterformcomplementarendereco(request)

    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()

            return render(request, 'cbv/cadastrousuario/complementarconcluido.html')

    return render(request,
                  'cbv/cadastrousuario/complementarendereco.html',
                  {'formulario':formulario})




############ Fim Experiencias ###########


############ Rede de Descontos ###########

def rededescontopublicados():
    from .models import RedeDeDesconto
    return RedeDeDesconto.objects.filter(Publicar=True).order_by('-DataPublicacao')

def rededescontos(request):
    from .forms import FormBuscaDesconto
    from .models import BannerRedeDesconto

    form = FormBuscaDesconto()

    conteudos = rededescontopublicados()

    bannerrede = BannerRedeDesconto.objects.filter(Ativo=True).first()

    if request.method == 'POST':
        form = FormBuscaDesconto(request.POST)
        form.is_valid()

        termos = form.cleaned_data['busca']

        conteudos = buscarpublicacao(conteudos, termos)

    return render(request,
                  'cbv/rededescontos/rededescontos.html',
                  {'conteudos': conteudos,
                   'bannerrede': bannerrede,
                   'form': form})

def detalherededescontos(request, categoria, id):
    from django.shortcuts import get_object_or_404, redirect
    from .models import RedeDeDesconto

    rede = get_object_or_404(RedeDeDesconto, id=id, Ativo=True)

    return redirect(rede.Link)

############ Fim Rede de Descontos ###########


############ Censo do Volei ###########

def censosvoleipublicados():
    from .models import CensoDoVolei
    return CensoDoVolei.objects.filter(Publicar=True).order_by('-DataPublicacao')

def censosvolei(request, ativo=None):
    from .models import BannerCensoDoVolei

    banner = BannerCensoDoVolei.objects.filter(Ativo=True).first()

    carrossel = censosvoleipublicados().filter(Destaque=True)[:5]

    censosvoleiativos = censosvoleipublicados().filter(Ativo=True)[:3]

    censosvoleiinativos = censosvoleipublicados().filter(Ativo=False)[:3]

    if ativo:
        censosvoleiinativos = []
        censosvoleiativos = censosvoleipublicados().filter(Ativo=True)

    return render(request,
                  'cbv/censosvolei/censosvolei.html',
                  {'banner': banner,
                   'censosvoleiativos': censosvoleiativos,
                   'censosvoleiinativos': censosvoleiinativos,
                   'conteudos_carrossel': carrossel,
                   'mostrarcompleto': True,
                   'ativo': ativo})

def censosvoleiinativos(request, ativo):
    from .forms import FormBuscaSimples

    form = FormBuscaSimples()

    conteudos = censosvoleipublicados().filter(Ativo=False)

    if request.method == 'POST':
        form = FormBuscaSimples(request.POST)
        form.is_valid()

        termos = form.cleaned_data['busca']

        conteudos = buscarpublicacao(conteudos, termos)

    return render(request,
                  'cbv/censosvolei/censosvoleiinativos.html',
                  {'conteudos':conteudos, 'form':form})

@obrigar_cadastro_complementar
def detalhecensovolei(request, categoria, id):
    from .forms import CadastroUsuarioBasicoForm, LoginForm
    conteudos = censosvoleipublicados()

    conteudo = conteudos.get(Categoria__slug=categoria, id=id)

    return render(request,
                  'cbv/censosvolei/detalhecensosvolei.html',
                  {'conteudo':conteudo,
                   'formcadastrobasico': CadastroUsuarioBasicoForm(),
                   'formlogin': LoginForm(),
                   'enderecocompleto': estariaenderecocompleto(request)})

############ Fim Censo do Volei ###########

############ Fale Conosco ###########

def faleconosco(request):
    from django.template.loader import get_template
    from django.core.mail import EmailMultiAlternatives
    from django.conf import settings
    from .forms import FaleConoscoForm

    form = FaleConoscoForm()

    if request.method == 'POST':
        form = FaleConoscoForm(request.POST)
        if form.is_valid():
            corpo = {'nome': form.cleaned_data['nome'],
                     'email': form.cleaned_data['email'],
                     'mensagem': form.cleaned_data['mensagem'],}

            html = get_template('cbv/faleconosco/emailfaleconosco.html')
            text = get_template('cbv/faleconosco/emailfaleconosco.txt')

            subject, from_email, to = 'Contato CBV', settings.EMAIL_HOST_USER, settings.CONTATOS
            html_content = html.render(corpo)
            text_content = text.render(corpo)

            msg = EmailMultiAlternatives(subject,
                                         text_content,
                                         from_email=from_email,
                                         bcc=to)

            msg.attach_alternative(html_content, "text/html")

            msg.send()

            return render(request, 'cbv/faleconosco/enviosucesso.html')

    return render(request, 'cbv/faleconosco/faleconosco.html', {'form': form})

############ Fim Fale Conosco ###########

