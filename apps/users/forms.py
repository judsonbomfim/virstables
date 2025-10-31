from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilCliente
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já existe.")
        return username

class PerfilClienteForm(forms.ModelForm):
    """Formulário para cadastro e edição de perfil de cliente"""
    nome_completo = forms.CharField(
        max_length=200,
        required=True,
        label="Nome Completo",
        help_text="Este nome será usado para preencher automaticamente o nome no sistema"
    )
    
    class Meta:
        model = PerfilCliente
        fields = [
            'nome_completo', 'cpf', 'cnpj', 'rg_ie', 'emis_uf', 'nasc_fund', 
            'profis_cnae', 'end_cep', 'end_rua_av', 
            'end_numero', 'end_complem', 'end_bairro', 'end_cidade', 'end_estado',
            'telefone', 'celular', 'propriedade', 'propr_cidade', 'propr_estado'
        ]
        widgets = {
            'nasc_fund': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
            'emis_uf': forms.Select(attrs={'class': 'form-control'}),
            'end_estado': forms.Select(attrs={'class': 'form-control'}),
            'propr_estado': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00', 'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'placeholder': '00.000.000/0000-00', 'class': 'form-control'}),
            'end_cep': forms.TextInput(attrs={'placeholder': '00000-000', 'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(11) 1234-5678', 'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'placeholder': '(11) 91234-5678', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        """Inicializa o formulário com os widgets corretos"""
        super().__init__(*args, **kwargs)
        
        # Define o formato de entrada para o campo de data
        self.fields['nasc_fund'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
        
        # Adiciona classe form-control a todos os campos que ainda não têm
        for field_name, field in self.fields.items():
            if field_name != 'nome_completo':  # nome_completo já é CharField
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
    
    def clean_cpf(self):
        """Valida se o CPF já está cadastrado, exceto para o próprio registro"""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove caracteres especiais
            cpf_limpo = cpf.replace('.', '').replace('-', '')
            
            # Verifica se já existe outro perfil com este CPF
            queryset = PerfilCliente.objects.filter(cpf=cpf)
            
            # Se estamos editando, exclui o próprio registro da busca
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError('Este CPF já está cadastrado.')
        
        return cpf
    
    def clean_cnpj(self):
        """Valida se o CNPJ já está cadastrado, exceto para o próprio registro"""
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            # Remove caracteres especiais
            cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
            
            # Verifica se já existe outro perfil com este CNPJ
            queryset = PerfilCliente.objects.filter(cnpj=cnpj)
            
            # Se estamos editando, exclui o próprio registro da busca
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError('Este CNPJ já está cadastrado.')
        
        return cnpj