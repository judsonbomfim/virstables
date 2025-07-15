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
                user = user_form.save()
                perfil = perfil_form.save(commit=False)
                perfil.usuario = user
                perfil.save()
                grupo_clientes = Group.objects.get(name='Clientes')
                user.groups.add(grupo_clientes)
                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('leilao_list')
            except ObjectDoesNotExist:
                messages.error(request, 'Erro: Grupo Clientes não encontrado.')
                return render(request, 'frontend/conta/cadastro.html', {'user_form': user_form, 'perfil_form': perfil_form})
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
        if self.request.user.groups.filter(name='Administradores').exists():
            return reverse_lazy('home_backend:home')  # Redireciona para o backend
        return reverse_lazy('home_frontend:home')  # Redireciona para o frontend