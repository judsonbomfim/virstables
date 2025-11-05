from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from core.decorators import group_required
from apps.users.models import PerfilCliente
from apps.users.forms import PerfilClienteForm  # <-- Usar o mesmo formulário
from django.contrib.auth.models import User

@login_required(login_url='/login/')
@group_required('Administradores')
def cliente_lista(request):
    """Lista todos os clientes cadastrados"""
    clientes = PerfilCliente.objects.all().select_related('usuario').order_by('-id')
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Clientes',
        'page_subtitle': 'Lista de Clientes',
        'page_icon': 'icofont icofont-users-social',
        'clientes': clientes,
    }
    
    return render(request, 'backend/users/cliente_lista.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def cliente_detalhe(request, id):
    """Exibe detalhes de um cliente"""
    perfil = get_object_or_404(PerfilCliente, id=id)
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Detalhes do Cliente',
        'page_subtitle': perfil.usuario.get_full_name() or perfil.usuario.username,
        'page_icon': 'icofont icofont-user-alt-3',
        'perfil': perfil,
    }
    
    return render(request, 'backend/users/cliente_detalhe.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def cliente_editar(request, id):
    """Edita informações de um cliente"""
    perfil = get_object_or_404(PerfilCliente, id=id)
    
    if request.method == 'POST':
        form = PerfilClienteForm(request.POST, instance=perfil)
        if form.is_valid():
            # Atualizar nome do usuário se fornecido
            nome_completo = form.cleaned_data.get('nome_completo', '').strip()
            if nome_completo:
                nomes = nome_completo.split()
                perfil.usuario.first_name = nomes[0] if nomes else ''
                perfil.usuario.last_name = ' '.join(nomes[1:]) if len(nomes) > 1 else ''
                perfil.usuario.save()
            
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('users_backend:cliente_detalhe', id=perfil.id)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # Preencher nome_completo inicial
        initial_data = {
            'nome_completo': f"{perfil.usuario.first_name} {perfil.usuario.last_name}".strip()
        }
        form = PerfilClienteForm(instance=perfil, initial=initial_data)
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Editar Cliente',
        'page_subtitle': perfil.usuario.get_full_name() or perfil.usuario.username,
        'page_icon': 'icofont icofont-edit',
        'form': form,
        'perfil': perfil,
    }
    
    return render(request, 'backend/users/cliente_editar.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def cliente_aprovar(request, id):
    """Aprova ou reprova um cliente"""
    perfil = get_object_or_404(PerfilCliente, id=id)
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        
        if acao == 'aprovar':
            perfil.usuario.is_active = True
            perfil.usuario.save()
            messages.success(request, f'Cliente {perfil.usuario.get_full_name()} aprovado com sucesso!')
        elif acao == 'reprovar':
            perfil.usuario.is_active = False
            perfil.usuario.save()
            messages.warning(request, f'Cliente {perfil.usuario.get_full_name()} foi desativado.')
    
    return redirect('users_backend:cliente_detalhe', id=perfil.id)