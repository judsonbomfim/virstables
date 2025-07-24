from email.headerregistry import Group
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from ..forms import CustomUserCreationForm, PerfilClienteForm

def cadastro(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        perfil_form = PerfilClienteForm(request.POST)
        
        if user_form.is_valid() and perfil_form.is_valid():
            try:
                # Criar o usuário
                user = user_form.save(commit=False)
                
                # Processar nome completo do PerfilCliente para first_name e last_name
                nome_completo = perfil_form.cleaned_data.get('nome_completo', '').strip()
                if nome_completo:
                    nomes = nome_completo.split()
                    user.first_name = nomes[0] if nomes else ''
                    user.last_name = ' '.join(nomes[1:]) if len(nomes) > 1 else ''
                
                user.is_active = True  # Inativo até aprovação
                user.save()
                
                # Criar o perfil
                perfil = perfil_form.save(commit=False)
                perfil.usuario = user
                perfil.save()
                
                messages.success(request, 
                    f'Cadastro realizado com sucesso para {user.first_name} {user.last_name}! '
                    'Sua conta está em análise.')
                return redirect('home_frontend:home')
                
            except Exception as e:
                messages.error(request, f'Erro ao realizar cadastro: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        user_form = CustomUserCreationForm()
        perfil_form = PerfilClienteForm()
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Cadastro de Cliente',
        'user_form': user_form,
        'perfil_form': perfil_form
    }

    return render(request, 'frontend/conta/cadastro.html', context)

class CustomLoginView(LoginView):
    template_name = 'frontend/conta/login.html'

    def get_success_url(self):
        # PRIMEIRO: Verificar se existe parâmetro 'next'
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        
        # SE NÃO HOUVER 'next', usar as regras de grupo
        if self.request.user.groups.filter(name='Administradores').exists():
            return reverse_lazy('home_backend:home')  # Redireciona para o backend
        return reverse_lazy('home_frontend:home')  # Redireciona para o frontend