from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilCliente
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Digite um email válido")
    username = forms.CharField(
        label="Usuário",
        help_text="Use apenas letras minúsculas e números, sem espaços ou acentos."
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email

class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        fields = [
            'cpf', 'cnpj', 'rg_ie', 'emis_uf', 'nasc_fund', 'profis_cnae',
            'representante', 'cpf_repres', 'end_cep', 'end_rua_av', 'end_numero',
            'end_complem', 'end_bairro', 'end_cidade', 'end_estado',
            'telefone', 'celular'
        ]
        widgets = {
            'nasc_fund': forms.DateInput(attrs={'type': 'date'}),
            'emis_uf': forms.Select(),
            'end_estado': forms.Select(),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'cnpj': forms.TextInput(attrs={'placeholder': '00.000.000/0000-00'}),
            'cpf_repres': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'end_cep': forms.TextInput(attrs={'placeholder': '00000-000'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(11) 1234-5678'}),
            'celular': forms.TextInput(attrs={'placeholder': '(11) 91234-5678'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if PerfilCliente.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if not cnpj:
            return cnpj  # Não valida se estiver vazio
        if PerfilCliente.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError("Este CNPJ já está cadastrado.")
        return cnpj

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PerfilCliente.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email