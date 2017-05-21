# coding=utf-8

from django import forms
from .models import InfosAdicionaisUsuario


class FormBuscaSimples(forms.Form):
    busca = forms.CharField(label="", required=False, max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Pesquisar'}))

class CadastroUsuarioBasicoForm(forms.Form):
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
    cpfpassaporte = forms.CharField(
        label="CPF|Passaporte",
        max_length=16,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'CPF|Passaporte'}))
    unidadefederativa = forms.CharField(
        label="UF",
        max_length=2,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'UF'}))
    password = forms.CharField(
        label="Senha",
        max_length=16,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Senha'}))
    passwordconfirm = forms.CharField(
        label="Confirmar Senha",
        max_length=16,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': u'Confirmação de Senha'}))

    def clean_email(self):
        from django.contrib.auth.models import User
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError(
                u'Já existe um cadastro com esse email.')

        return data

    def clean(self):
        from django.contrib.auth import password_validation

        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['passwordconfirm']

        if pass1 and pass1 != pass2:
            raise forms.ValidationError(u'As senhas não são idênticas.')

        password_validation.validate_password(self.cleaned_data['password'])

        return self.cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-Mail",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'E-Mail'}))

    password = forms.CharField(
        label="Senha",
        max_length=16,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Senha'}))

    def clean(self):
        from django.contrib.auth.models import User

        usuarios = User.objects.filter(email=self.cleaned_data['email'])

        if usuarios.count() == 0 or \
            not usuarios[0].check_password(self.cleaned_data['password']):
            raise forms.ValidationError(u"Email ou senha invalido")

class CadastroComplementar(forms.ModelForm):
    class Meta:
        model = InfosAdicionaisUsuario
        exclude = ['user']


    def __init__(self, *args, **kwargs):
        from django.core.validators import RegexValidator
        super(CadastroComplementar, self).__init__(*args, **kwargs)

        self.fields['cpf'].required = True
        self.fields['tipodocumento'].required = True
        self.fields['ufed'].required = True
        self.fields['sexo'].required = True
        self.fields['celular'].required = True
        self.fields['telefone'].required = True
        self.fields['cep'].validators = [RegexValidator(regex=r'^(\d{5}|\d{8})$',
                                                        message=u'CEP deve conter 5 ou 8 dígitos',
                                                        code='nomatch')]
        self.fields['modalidade_favorita'].required = True

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.help_text if field.help_text else field.label
                })
