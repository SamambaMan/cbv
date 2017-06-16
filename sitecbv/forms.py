# coding=utf-8

from django import forms
from django.forms import SelectMultiple, Select
from .models import InfosAdicionaisUsuario, UF_CHOICES


class FormBuscaSimples(forms.Form):
    busca = forms.CharField(label="", required=False, max_length=50, widget=forms.TextInput(
        attrs={'class':'inputPesquisa',
               'placeholder':'O que você está procurando?',
               'type':'txt'}))

class FormBuscaDesconto(FormBuscaSimples):

    def __init__(self, *args, **kwargs):
        super(FormBuscaDesconto, self).__init__(*args, **kwargs)
        self.fields['busca'].widget.attrs.update({'placeholder':'O que você quer comprar com seu desconto?'})

def validate(password):
    import string
    letters = set(string.ascii_letters)
    digits = set(string.digits)
    pwd = set(password)
    return not (pwd.isdisjoint(letters) or pwd.isdisjoint(digits))

class CadastroUsuarioBasicoForm(forms.Form):
    firstname = forms.CharField(
        label="Nome Completo",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nome', 'class':'box1'}))
    email = forms.EmailField(
        label="E-Mail",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'E-Mail', 'class':'box1'}))
    cpfpassaporte = forms.CharField(
        label="CPF|Passaporte",
        max_length=16,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'CPF|Passaporte', 'class':'box2'}))
    unidadefederativa = forms.CharField(
        label="UF",
        max_length=2,
        required=True,
        widget=forms.Select(choices=UF_CHOICES, attrs={'class':'box2'}))
    password = forms.CharField(
        label="Senha",
        max_length=16,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Senha', 'class':'box2'}))
    passwordconfirm = forms.CharField(
        label="Confirmar Senha",
        max_length=16,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': u'Confirmação de Senha', 'class':'box2'}))

    def clean_email(self):
        from django.contrib.auth.models import User
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError(
                u'Já existe um cadastro com esse email.')

        return data


    def clean(self):
        from .snipets import validate_CPF
        from .models import InfosAdicionaisUsuario
        import string

        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['passwordconfirm']

        if pass1 and pass1 != pass2:
            raise forms.ValidationError(u'As senhas não são idênticas.')

        if self.cleaned_data['unidadefederativa'] != "FO":
            validate_CPF(self.cleaned_data['cpfpassaporte'])

        letters = set(string.ascii_letters)
        digits = set(string.digits)
        pwd = set(self.cleaned_data['password'])

        if not self.cleaned_data['password'] or len(self.cleaned_data['password']) < 8:
            raise forms.ValidationError(u"A senha deve conter pelo menos 8 caracteres")

        if not validate(self.cleaned_data['password']):
            raise forms.ValidationError(u"A senha deve conter letras e números")

        if InfosAdicionaisUsuario.objects.filter(cpf=self.cleaned_data['cpfpassaporte']).count() > 0:
            raise forms.ValidationError(u'Já existe um CPF/Passaporte cadastrado com esse número.')

        return self.cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-Mail",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'E-Mail', 'class':'box1', 'autocomplete':'off'}))

    password = forms.CharField(
        label="Senha",
        max_length=16,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Senha', 'class':'box1', 'autocomplete':'off'}))

    def clean(self):
        from django.contrib.auth.models import User

        if self.is_valid():

            usuarios = User.objects.filter(email=self.cleaned_data['email'])

            if usuarios.count() == 0 or \
                not usuarios[0].check_password(self.cleaned_data['password']):
                raise forms.ValidationError(u"Email ou senha invalido")

def rendergroupedselect(self, multiple, name, value, attrs=None, choices=()):
    from django.utils.html import format_html, escape
    from django.utils.encoding import smart_unicode
    from django.utils.safestring import mark_safe
    from django.forms.utils import flatatt
    from .models import SUPERLIGA_CHOICE

    if not isinstance(value, list):
        value = [value]
    value = map(str, value)

    extraattrs = {'name':name,}
    if multiple:
        extraattrs.update({'multiple':'multiple'})

    if value is None:
        value = ''
    final_attrs = self.build_attrs(attrs, extraattrs)
    output = [format_html('<select{0} class="form-control">', flatatt(final_attrs))]

    grupo_inicial = ""

    if not multiple:
        output.append('<option value="">--------</option>')

    for option in self.choices.queryset.order_by('Nome').order_by('Superliga'):
        if unicode(option.Superliga) != grupo_inicial:
            if grupo_inicial != "":
                output.append(u'</optgroup>')

            output.append('<optgroup label = "%s">' % escape(smart_unicode(dict(SUPERLIGA_CHOICE)[option.Superliga])))
            grupo_inicial = option.Superliga

        option_value = smart_unicode(option.id)
        option_label = smart_unicode(option.Nome)
        selected = ""
        
        if option_value in value:
            selected = "selected"
        output.append(u'<option value="%s" %s>%s</option>' % (escape(option_value), selected, escape(option_label)))

    output.append(u'</optgroup>')
    output.append(u'</select>')
    return mark_safe('\n'.join(output))


class GroupedMultipleSelectTime(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        return rendergroupedselect(self, True, name, value, attrs, choices)

class GroupedSelectTime(Select):
    def render(self, name, value, attrs=None, choices=()):
        return rendergroupedselect(self, False, name, value, attrs, choices)

class CadastroComplementar(forms.ModelForm):
    firstname = forms.CharField(
        label="Nome",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nome'}))

    email = forms.EmailField(
        label="E-Mail",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'E-Mail'}))

    senhaantiga = forms.CharField(
        label="Senha Antiga",
        max_length=16,
        required=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Senha'}))

    senhanova = forms.CharField(
        label="Senha Nova",
        max_length=16,
        required=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Senha'}))
    
    confirmacaosenha = forms.CharField(
        label="Confirmacao de Senha",
        max_length=16,
        required=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Senha'}))

    class Meta:
        model = InfosAdicionaisUsuario
        exclude = ['user', 'tipodocumento', 'cadastrocompleto']

    def clean(self):
        super(CadastroComplementar, self).clean()

        if self.cleaned_data['modalidade_favorita'] == 'VQ':
            if not self.cleaned_data['time_favorito_masculino']\
                or not self.cleaned_data['time_favorito_feminino']:
                self.add_error(
                    'modalidade_favorita',
                    "Selecione um time favorito masculino e um time favorito feminino")
        elif self.cleaned_data['modalidade_favorita'] == 'VP':
            if not self.cleaned_data['jogador_favorito']\
                or not self.cleaned_data['jogadora_favorita']:
                self.add_error('modalidade_favorita', "Escolha um jogador e uma jogadora favoritos")
        else:
            if not self.cleaned_data['jogador_favorito']\
                or not self.cleaned_data['jogadora_favorita']\
                or not self.cleaned_data['time_favorito_masculino']\
                or not self.cleaned_data['time_favorito_feminino']:
                self.add_error('modalidade_favorita', "Escolha seus jogadores e times favoritos")

	if self.cleaned_data['senhaantiga'] or self.cleaned_data['senhanova'] or self.cleaned_data['confirmacaosenha']\
	   and ( not self.cleaned_data['senhaantiga'] or not self.cleaned_data['senhanova'] or not self.cleaned_data['confirmacaosenha']):
	    self.add_error('senhaantiga',u'Informe todos os campos obrigatórios')
        else:
        
            if self.cleaned_data['senhaantiga']:
                if not self.instance.user.check_password(self.cleaned_data['senhaantiga']):
                    self.add_error('senhaantiga', u'Senha antiga inválida')
                else:
                    if not self.cleaned_data['senhanova']:
                        self.add_error('senhanova', u'Informe uma senha nova')
                    elif self.cleaned_data['senhanova'] != self.cleaned_data['confirmacaosenha']:
                        self.add_error('senhanova', u'As senhas informadas não conferem')

        
    def __init__(self, *args, **kwargs):
        from django.core.validators import RegexValidator

        instance = kwargs.get('instance', None)

        kwargs.update(initial={
            'firstname': instance.user.first_name,
            'email': instance.user.email,
        })

        super(CadastroComplementar, self).__init__(*args, **kwargs)

        attrs_telefone = {
            'onKeyDown': 'Mascara(this,Celular)',
            'onKeyPress': 'Mascara(this,Celular);',
            'onKeyUp': 'Mascara(this,Celular)',
            'maxlength': '15',
        }

        self.fields['email'].disabled = True
        self.fields['cpf'].required = True
        self.fields['ufed'].required = True
        self.fields['sexo'].required = True
        self.fields['celular'].widget.attrs.update(attrs_telefone)
        self.fields['telefone'].widget.attrs.update(attrs_telefone)

        self.fields['times_secundarios_masculino'].widget = GroupedMultipleSelectTime()
        self.fields['times_secundarios_feminino'].widget = GroupedMultipleSelectTime()
        self.fields['time_favorito_masculino'].widget = GroupedSelectTime()
        self.fields['time_favorito_feminino'].widget = GroupedSelectTime()


        self.fields['nascimento'].input_formats = ['%d/%m/%Y']
        self.fields['nascimento'].widget.attrs.update({
            'onKeyDown': 'Mascara(this,Data)',
            'onKeyPress': 'Mascara(this,Data);',
            'onKeyUp': 'Mascara(this,Data)',
            'maxlength': '10',
        })

        self.fields['cep'].validators = [RegexValidator(
            regex=r'^(\d{5}|\d{5}-\d{3})$',
            message=u'CEP no formato 00000 ou 00000-000',
            code='nomatch')]
        self.fields['cep'].widget.attrs.update({
            'onKeyDown': 'Mascara(this,Cep)',
            'onKeyPress': 'Mascara(this,Cep);',
            'onKeyUp': 'Mascara(this,Cep)',
            'maxlength': '9',
        })

        self.fields['modalidade_favorita'].required = True


        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and field_name != "receberinformacoesprograma":
                field.widget.attrs.update({
                    'placeholder': field.label,
                    'class': 'form-control',
                })

        if self.instance and self.instance.cadastrocompleto:
            self.fields['cpf'].disabled = self.fields['ufed'].disabled = True


class FormComplementarEndereco(forms.ModelForm):
    class Meta:
        model = InfosAdicionaisUsuario
        fields = ['cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'pais', 'ufed']


    def __init__(self, *args, **kwargs):
        from django.core.validators import RegexValidator

        super(FormComplementarEndereco, self).__init__(*args, **kwargs)

        self.fields['ufed'].required = True
        self.fields['ufed'].disabled = True

        self.fields['cep'].required = True
        self.fields['endereco'].required = True
        self.fields['numero'].required = True
        self.fields['bairro'].required = True
        self.fields['cidade'].required = True
        self.fields['pais'].required = True

        self.fields['cep'].validators = [RegexValidator(
            regex=r'^(\d{5}|\d{5}-\d{3})$',
            message=u'CEP no formato 00000 ou 00000-000',
            code='nomatch')]
        self.fields['cep'].widget.attrs.update({
            'onKeyDown': 'Mascara(this,Cep)',
            'onKeyPress': 'Mascara(this,Cep);',
            'onKeyUp': 'Mascara(this,Cep)',
            'maxlength': '9',
        })

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.label,
                    'class': 'form-control',
                })

class FaleConoscoForm(forms.Form):
    nome = forms.CharField(
        label="Nome",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'class':'form-control'}))
    email = forms.EmailField(
        label="E-Mail",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'class':'form-control'}))
    mensagem = forms.CharField(
        label="Mensagem",
        max_length=4000,
        required=True,
        widget=forms.Textarea(
            attrs={'class':'form-control'}))
