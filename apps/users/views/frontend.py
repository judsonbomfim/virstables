from email.headerregistry import Group
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.auth.models import User
from apps.emails.tasks import email_cadastro_analise, email_recuperacao_senha
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
                
                user.is_active = True
                user.save()
                
                # Criar o perfil
                perfil = perfil_form.save(commit=False)
                perfil.usuario = user
                perfil.save()

                email_cadastro_analise.delay(perfil.id)

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
            return reverse_lazy('home_backend:home')
        return reverse_lazy('home_frontend:home')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'frontend/conta/password_reset.html'
    success_url = reverse_lazy('users_frontend:password_reset_done')
    from_email = settings.DEFAULT_FROM_EMAIL
    
    def form_valid(self, form):
        """Override para enviar e-mail via Celery"""
        # Não chama o super().form_valid() para evitar envio de e-mail padrão
        email = form.cleaned_data['email']
        users = User.objects.filter(email=email, is_active=True)
        
        if users.exists():
            for user in users:
                # Gera o token de reset
                from django.contrib.auth.tokens import default_token_generator
                from django.utils.http import urlsafe_base64_encode
                from django.utils.encoding import force_bytes
                
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Enviar e-mail via Celery
                email_recuperacao_senha.delay(user.id, uid, token)
        
        # Redireciona para a página de confirmação
        return redirect(self.success_url)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'frontend/conta/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'frontend/conta/password_reset_confirm.html'
    success_url = reverse_lazy('users_frontend:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'frontend/conta/password_reset_complete.html'