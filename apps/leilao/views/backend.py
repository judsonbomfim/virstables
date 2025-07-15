import os
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm, Select
from django.forms import ModelForm
from django.conf import settings
from core.decorators import group_required
from apps.leilao.models import Leilao, Lance
from apps.cavalo.models import Cavalo

class LeilaoForm(ModelForm):
    class Meta:
        model = Leilao
        fields = ['nome', 'descricao', 'termos', 'data_leilao', 'data_inicio', 'data_fim', 'imagem', 'status']
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'termos': forms.Textarea(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-select'}),
        }

@login_required(login_url='/login/')
@group_required('Administradores')
def leilao_lista(request):
    leiloes_ativ = Leilao.objects.filter(status='ativo').order_by('data_fim')
    leiloes_dest = Leilao.objects.exclude(status='ativo').order_by('data_fim')
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Listar Leilões',
        'page_icon': 'icofont icofont-court-hammer',
        'pagesub_title': 'Detalhe Leilão',
        'leiloes_ativ': leiloes_ativ,
        'leiloes_dest': leiloes_dest,
    }
    
    return render(request, 'backend/leilao_lista.html', context)

@login_required(login_url='/login/')
@group_required('Administradores')
def leilao_detalhe(request, id):
    leilao = Leilao.objects.get(pk=id)
    cavalos = leilao.cavalos_leilao.all()
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Leilão - {leilao.nome}',
        'page_icon': 'icofont icofont-court-hammer',
        'pagesub_title': 'Detalhe Leilão',
        'leilao': leilao,
        'cavalos': cavalos,
    }
    
    if request.method == 'POST':
        cavalo_id = request.POST.get('cavalo_id')
        valor = request.POST.get('valor')
        try:
            cavalo = Cavalo.objects.get(pk=cavalo_id, leilao=leilao)
            lance = Lance(cavalo=cavalo, usuario=request.user, valor=valor)
            lance.clean()
            lance.save()
        except Exception as e:
            context.update({'error': str(e)})
            return render(request, 'backend/leilao_detalhe.html', context)
        
    return render(request, 'backend/leilao_detalhe.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def leilao_form(request, id=None):
    if request.method == 'POST':
        if id:
            leilao = get_object_or_404(Leilao, pk=id)
            imagem_antiga = leilao.imagem.path if leilao.imagem else None
            # if not request.user.has_perm('core.change_leilao', leilao):
            #     raise PermissionDenied("Você não tem permissão para editar este leilão.")
            form = LeilaoForm(request.POST, request.FILES, instance=leilao)
            print("Form data:", request.POST)  # Debug
            print("FILES:", request.FILES)
            if form.is_valid():
                if 'imagem' in request.FILES and imagem_antiga:
                    if os.path.isfile(imagem_antiga):
                        os.remove(imagem_antiga)
                        print(f"Imagem antiga removida: {imagem_antiga}")
                leilao = form.save(commit=False)
                leilao.save()
                return redirect('leilao:leilao_detalhe', id=leilao.pk)
            else:
                print("Erros do form:", form.errors)
        else:   
            form = LeilaoForm(request.POST)
            if form.is_valid():
                leilao = form.save(commit=False)
                leilao.save()
                return redirect('leilao:leilao_detalhe', id=leilao.pk)
            else:
                print("Erros do form:", form.errors)  # Debug
    else:        
        if id:
            leilao = get_object_or_404(Leilao, pk=id)            
            page_subtitle = 'Editar Leilão'
            form = LeilaoForm(instance=leilao)
        else:
            form = LeilaoForm()
            page_subtitle = 'Adicionar Leilão'
        
        
        context = {
            'painel_title': settings.PAINEL_TITLE,
            'page_title': 'Leilão',
            'page_subtitle': page_subtitle,
            'page_icon': 'icofont icofont-court-hammer',
            'form': form,
            'leilao': leilao if id else None,
        }
        
        return render(request, 'backend/leilao_form.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def leilao_excluir(request, id):
    leilao = get_object_or_404(Leilao, pk=id)
    if request.method == 'POST':
        leilao.delete()
        return redirect('leilao:leilao_lista')