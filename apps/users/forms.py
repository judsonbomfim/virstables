from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilCliente
import re

class CustomUserCreationForm(UserCreationForm):
    nome_completo = forms.CharField(
        max_length=100, 
        required=True, 
        label="Nome Completo",
        help_text="Digite seu nome completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: João Silva Santos'})
    )
    email = forms.EmailField(
        required=True, 
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'nome_completo', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: joaosilva'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Apenas letras minúsculas e números, sem espaços"
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise forms.ValidationError("O usuário não pode conter espaços.")
        if username.upper() != username.lower():
            raise forms.ValidationError("O usuário deve conter apenas letras minúsculas.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já existe.")
        return username.lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Processar o nome completo
        nome_completo = self.cleaned_data['nome_completo'].strip()
        nomes = nome_completo.split()
        
        if nomes:
            user.first_name = nomes[0]
            user.last_name = ' '.join(nomes[1:]) if len(nomes) > 1 else ''
        
        if commit:
            user.save()
        return user

class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        exclude = ['usuario']  # Excluir o campo usuario do formulário
        widgets = {
            'emis_uf': forms.Select(attrs={'class': 'form-select'}),
            'end_estado': forms.Select(attrs={'class': 'form-select'}),
            'propr_estado': forms.Select(attrs={'class': 'form-select'}),
            'nasc_fund': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar alguns campos opcionais se necessário
        self.fields['cnpj'].required = False
        self.fields['telefone'].required = False
        self.fields['profis_cnae'].required = False
        self.fields['end_complem'].required = False
        self.fields['propriedade'].required = False
        self.fields['propr_cidade'].required = False
        self.fields['propr_estado'].required = False

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