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
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['passwordconfirm']

        if pass1 and pass1 != pass2:
            raise forms.ValidationError(u'As senhas não são idênticas.')

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
        
    def clean(): 
        pass #TODO: falta implementar

class CadastroComplementar(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CadastroComplementar, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.help_text if field.help_text else field.label
                })

    class Meta:
        model = InfosAdicionaisUsuario
        exclude = ['cadastrocompleto']
