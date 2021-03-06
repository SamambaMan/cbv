# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .decorators import obrigar_cadastro_complementar
from django.contrib.auth.decorators import user_passes_test


def torcidometro_times():
    from django.db.models import F, Count
    from .models import Time

    todos_times = Time.objects.filter().exclude(Nenhum=True)

    somatimes = todos_times.annotate(qtd_masculino=Count('infos_time_favorito_masculino'))
    somatimes = somatimes.annotate(qtd_feminino=Count('infos_time_favorito_feminino'))
    somatimes = somatimes.annotate(soma=F('qtd_masculino') + F('qtd_feminino')).order_by('-soma')

    valortotal = 0.0
    for atual in somatimes.values_list('soma'):
        valortotal = valortotal + atual[0]

    if valortotal != 0.0:
        somatimes = somatimes.annotate(percentual=(F('soma') * 100.0)/valortotal)
    else:
        somatimes = somatimes.annotate(percentual=F('soma'))

    return somatimes[:10]

def torcidometro_modalidades():
    from .models import InfosAdicionaisUsuario
    qtd_quadra = InfosAdicionaisUsuario.objects.filter(modalidade_favorita='VQ').count()
    qtd_praia = InfosAdicionaisUsuario.objects.filter(modalidade_favorita='VP').count()
    qtd_ambos = InfosAdicionaisUsuario.objects.filter(modalidade_favorita='AM').count()
    total = float(qtd_quadra + qtd_praia + qtd_ambos)

    qtd_quadra = round(qtd_quadra * 100.0 / total)
    qtd_praia = round(qtd_praia * 100.0 / total)
    qtd_ambos = round(qtd_ambos * 100.0 / total)

    return {'quadra': int(qtd_quadra), 'praia': int(qtd_praia), 'ambos': int(qtd_ambos)}

@obrigar_cadastro_complementar
def index(request):
    from .forms import CadastroUsuarioBasicoForm, LoginForm
    from .models import BannerHome, Beneficio
    from itertools import chain

    #conteudos_carrossel = conteudospublicados().filter(
    #    Destaque=True)[:5]

    conteudos_carrossel = BannerHome.objects.filter(Ativo=True).order_by('-id')

    #conteudos_experiencias = experienciaspublicadas().filter(Destaque=True)[:5]

    #conteudos_censo = censosvoleipublicados().filter(Destaque=True)[:5]

    #lista_total = sorted(
    #        chain(conteudos_carrossel,  conteudos_experiencias, conteudos_censo),
    #        key= lambda cont: cont.DataPublicacao, reverse=True)

    #conteudos_carrossel = lista_total[:5]


    return render(request, 'cbv/index.html',
                  {'formcadastrobasico': CadastroUsuarioBasicoForm(),
                   'formlogin': LoginForm(),
                   'conteudos_carrossel': conteudos_carrossel,
                   'torc_mod': torcidometro_modalidades(),
                   'torc_times': torcidometro_times(),
                   'beneficios': Beneficio.objects.filter(Ativo=True).order_by('Ordem')})


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
    from .models import Programa, Beneficio
    programas = Programa.objects.filter(Publicar=True)

    prg = None
    if programas.count() > 0:
        prg = programas[0]

    return render(request, 'cbv/programa.html', 
                  {'programa': prg,
                   'beneficios': Beneficio.objects.filter(Ativo=True).order_by('Ordem')})


def conteudospublicados():
    from .models import ConteudoExclusivo
    return ConteudoExclusivo.objects.filter(Publicar=True).order_by('-DataPublicacao')

@obrigar_cadastro_complementar
def conteudoexclusivo(request):
    from .models import ConteudoExclusivo, CategoriaConteudoExclusivo, BannerConteudoExclusivo
    from .forms import FormBuscaSimples

    conteudos_exibir = []
    for categoria in CategoriaConteudoExclusivo.objects.all():
        conteudos = conteudospublicados().filter(Categoria=categoria).order_by('-DataPublicacao')
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

    jogadores = Jogador.objects.filter(Sexo='M').order_by('-Nenhum')
    jogadoras = Jogador.objects.filter(Sexo='F').order_by('-Nenhum')
    timesm = Time.objects.filter(Sexo='M')
    timesf = Time.objects.filter(Sexo='F')

    if request.method == 'POST':
        formulario = CadastroComplementar(request.POST, instance=usuario.infosadicionaisusuario)
    else:
        formulario = CadastroComplementar(instance=usuario.infosadicionaisusuario)

    formulario.fields["jogador_favorito"].queryset = jogadores
    formulario.fields["jogadora_favorita"].queryset = jogadoras
    formulario.fields["jogadores_secundario_masculinos"].queryset = jogadores.exclude(Nenhum=True)
    formulario.fields["jogadoras_secundarias_femininas"].queryset = jogadoras.exclude(Nenhum=True)

    formulario.fields["time_favorito_masculino"].queryset = timesm
    formulario.fields["time_favorito_feminino"].queryset = timesf
    formulario.fields["times_secundarios_masculino"].queryset = timesm.exclude(Nenhum=True)
    formulario.fields["times_secundarios_feminino"].queryset = timesf.exclude(Nenhum=True)

    return formulario

def enviaremailcadastrocomplementar(request):
    from django.template.loader import get_template
    from django.core.mail import EmailMultiAlternatives
    from django.conf import settings

    corpo = {'nome': request.user.first_name,
             'endereco': settings.ENDERECO}

    html = get_template('cbv/cadastrousuario/email_cadcomplementar.html')
    text = get_template('cbv/cadastrousuario/email_cadcomplementar.txt')

    subject, from_email, to = u'Bem Vindo ao Eu Sou do Vôlei', settings.EMAIL_HOST_USER, [request.user.email]
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
    from django.shortcuts import redirect

    formulario = obterformcomplementar(request)
    completado = False
    senhaalterada = False

    if request.method == 'POST':
        if formulario.is_valid():

            antigo = InfosAdicionaisUsuario.objects.get(id=formulario.instance.id).cadastrocompleto

            informacoes = formulario.save()

            if formulario.cleaned_data['senhanova']:
                usuario = User.objects.get(id=request.user.id)
                usuario.set_password(formulario.cleaned_data['senhanova'])
                usuario.save()
                login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')
                senhaalterada = True


            if not antigo:
                informacoes.cadastrocompleto = True
                informacoes.save()
                enviaremailcadastrocomplementar(request)
                completado = True

            if completado:
                return redirect('/')

            return render(request,
                  'cbv/cadastrousuario/cadastrocomplementar.html',
                  {'formulario':formulario,
                   'completo':request.user.infosadicionaisusuario.cadastrocompleto,
                   'sucesso': True,
                   'completado': completado,
                   'senhaalterada': senhaalterada})

    return render(request,
                  'cbv/cadastrousuario/cadastrocomplementar.html',
                  {'formulario':formulario,
                   'completo':request.user.infosadicionaisusuario.cadastrocompleto})



############ Experiencias ##############

def experienciaspublicadas():
    from .models import Experiencia
    return Experiencia.objects.filter(Publicar=True).order_by('-DataPublicacao')

@obrigar_cadastro_complementar
def experiencias(request):
    from .models import BannerExperiencia
    from .forms import FormBuscaSimples

    experiencias_exibir = experienciaspublicadas().order_by('-Ativo', '-DataPublicacao')[:6]

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

    conteudos = experienciaspublicadas().order_by('-Ativo')

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

@obrigar_cadastro_complementar
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

@obrigar_cadastro_complementar
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

@obrigar_cadastro_complementar
def censosvolei(request):
    from .models import BannerCensoDoVolei

    banner = BannerCensoDoVolei.objects.filter(Ativo=True).first()

    carrossel = censosvoleipublicados().filter(Destaque=True)[:5]

    censosvoleiativos = censosvoleipublicados().filter(Ativo=True)[:3]

    censosvoleiinativos = censosvoleipublicados().filter(Ativo=False)[:3]

    return render(request,
                  'cbv/censosvolei/censosvolei.html',
                  {'banner': banner,
                   'censosvoleiativos': censosvoleiativos,
                   'censosvoleiinativos': censosvoleiinativos,
                   'conteudos_carrossel': carrossel,
                   'mostrarcompleto': True})

@obrigar_cadastro_complementar
def maiscensosvolei(request, ativo):
    from .forms import FormBuscaSimples

    form = FormBuscaSimples()

    conteudos = censosvoleipublicados().filter(Ativo=ativo == "ativos")

    if request.method == 'POST':
        form = FormBuscaSimples(request.POST)
        form.is_valid()

        termos = form.cleaned_data['busca']

        conteudos = buscarpublicacao(conteudos, termos)

    return render(request,
                  'cbv/censosvolei/catcensosvolei.html',
                  {'conteudos':conteudos,
                   'form':form,
                   'ativo':ativo})

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

            return render(request, 'cbv/faleconosco/faleconosco.html',
                          {'form': FaleConoscoForm(), 'enviado': True})

    return render(request, 'cbv/faleconosco/faleconosco.html', {'form': form})

############ Fim Fale Conosco ###########

##### consulta de cpf ####

def consultacpf(request, cpf):
    from .models import InfosAdicionaisUsuario
    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse

    usuario = get_object_or_404(InfosAdicionaisUsuario, cpf=cpf)

    return  JsonResponse([{'ativo': usuario.user.is_active and usuario.cadastrocompleto}], safe=False)

@user_passes_test(lambda u:u.is_staff, login_url='admin:login')
def relatoriocadastro(request):
    from .forms import FiltroRelatorioCadastro
    from .models import InfosAdicionaisUsuario
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    form = FiltroRelatorioCadastro(initial={'page':1})

    saida = None

    if request.method == 'POST':
        form = FiltroRelatorioCadastro(request.POST, initial={'page':1})
        if form.is_valid():
            resultados = InfosAdicionaisUsuario.objects.filter()
            if form.cleaned_data['nome']: resultados = resultados.filter(user__first_name__icontains=form.cleaned_data['nome'])
            if form.cleaned_data['email']: resultados = resultados.filter(user__email__icontains=form.cleaned_data['email'])
            if form.cleaned_data['cadastrocompleto']: resultados = resultados.filter(cadastrocompleto=True)
            if form.cleaned_data['cpf']: resultados = resultados.filter(cpf__icontains=form.cleaned_data['cpf'])
            if form.cleaned_data['celular']: resultados = resultados.filter(celular__icontains=form.cleaned_data['celular'])
            if form.cleaned_data['nascimento_ini']: resultados = resultados.filter(nascimento__gte=form.cleaned_data['nascimento_ini'])
            if form.cleaned_data['nascimento_fin']: resultados = resultados.filter(nascimento__lte=form.cleaned_data['nascimento_fin'])
            if form.cleaned_data['sexo']: resultados = resultados.filter(sexo=form.cleaned_data['sexo'])
            if form.cleaned_data['ufed']: resultados = resultados.filter(ufed=form.cleaned_data['ufed'])
            if form.cleaned_data['cidade']: resultados = resultados.filter(cidade__icontains=form.cleaned_data['cidade'])
            if form.cleaned_data['cep']: resultados = resultados.filter(cep__icontains=form.cleaned_data['cep'])
            if form.cleaned_data['endereco']: resultados = resultados.filter(endereco__icontains=form.cleaned_data['endereco'])
            if form.cleaned_data['numero']: resultados = resultados.filter(numero=form.cleaned_data['numero'])
            if form.cleaned_data['bairro']: resultados = resultados.filter(bairro__icontains=form.cleaned_data['bairro'])

            exp = request.GET.get('exp')
            if exp == '1':
                return exportarcsv(resultados)

            paginator = Paginator(resultados, 25)
            page = form.cleaned_data['page']

            try:
                saida = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                saida = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                saida = paginator.page(paginator.num_pages)


    
    return render(request, 
                  'cbv/relatoriocadastro.html',
                  {'form':form,
                   'resultados':saida,
                   'site_header':u"Confederação Brasileira de Volei"})

def exportarcsv(resultados):
    import csv
    import io
    from django.shortcuts import HttpResponse

    buffer = io.BytesIO()
    wr = csv.writer(buffer, quoting=csv.QUOTE_ALL)
    
    linhas = [['Nome','EMail','Ativo','Cad. Completo','CPF','Nascimento','Sexo','Cidade',
               'CEP','Endereco','Numero','Complemento','Bairro','UF','Time Favorito Feminino',
               'Time Favorito Masculino','Times Secundários Femininos', 'Times Secundários Masculinos']]
    for result in resultados:
        linhas += [[
            result.user.first_name,
            result.user.email,
            result.user.is_active,
            result.cadastrocompleto,
            result.cpf,
            result.nascimento,
            result.sexo,
            result.cidade,
            result.cep,
            result.endereco,
            result.numero,
            result.complemento,
            result.bairro,
            result.ufed,
            result.time_favorito_feminino if result.time_favorito_feminino else None,
            result.time_favorito_masculino if result.time_favorito_masculino else None,
            ', '.join(result.times_secundarios_feminino.all().values_list('Nome', flat=True)),
            ', '.join(result.times_secundarios_masculino.all().values_list('Nome', flat=True))
        ]]

    wr.writerows(linhas)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment;  filename=usuarios.csv'

    return response