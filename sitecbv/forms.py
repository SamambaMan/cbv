# coding=utf-8

from django import forms
from .models import InfosAdicionaisUsuario, UF_CHOICES


class FormBuscaSimples(forms.Form):
    busca = forms.CharField(label="", required=False, max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Pesquisar'}))

class CadastroUsuarioBasicoForm(forms.Form):
    firstname = forms.CharField(
        label="Nome",
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
        from django.contrib.auth import password_validation
        from .snipets import validate_CPF
        from .models import InfosAdicionaisUsuario

        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['passwordconfirm']

        if pass1 and pass1 != pass2:
            raise forms.ValidationError(u'As senhas não são idênticas.')

        if self.cleaned_data['unidadefederativa'] != "FO":
            validate_CPF(self.cleaned_data['cpfpassaporte'])

        password_validation.validate_password(self.cleaned_data['password'])

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

    class Meta:
        model = InfosAdicionaisUsuario
        exclude = ['user', 'tipodocumento']


    def __init__(self, *args, **kwargs):
        from django.core.validators import RegexValidator

        instance = kwargs.get('instance', None)

        kwargs.update(initial={
            'firstname': instance.user.first_name,
            'email': instance.user.email,
        })

        super(CadastroComplementar, self).__init__(*args, **kwargs)

        self.fields['email'].disabled = True
        self.fields['cpf'].required = True
        self.fields['ufed'].required = True
        self.fields['sexo'].required = True
        self.fields['celular'].required = True
        self.fields['telefone'].required = True
        self.fields['nascimento'].widget.attrs.update({
            'onKeyDown': 'Mascara(this,Data)',
            'onKeyPress': 'Mascara(this,Data);',
            'onKeyUp': 'Mascara(this,Data)',
            'maxlength': '10',
        })
        self.fields['nascimento'].input_formats = ['%d/%m/%Y']
        self.fields['cep'].validators = [RegexValidator(regex=r'^(\d{5}|\d{8})$',
                                                        message=u'CEP deve conter 5 ou 8 dígitos',
                                                        code='nomatch')]
        self.fields['modalidade_favorita'].required = True


        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.label,
                    'class': 'form-control',
                })

        if self.instance and self.instance.cadastrocompleto:
            self.fields['cpf'].disabled = self.fields['ufed'].disabled = True


