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
            'termos': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),  # CORREÇÃO: FileInput para upload
            'data_leilao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'data_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'data_fim': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'status': Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar o campo termos opcional
        self.fields['termos'].required = False
        self.fields['termos'].help_text = "Arquivo PDF com os termos do leilão (opcional)"

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
    leilao = get_object_or_404(Leilao, pk=id)
    
    # Buscar cavalos que têm lances neste leilão
    lances = Lance.objects.filter(leilao=leilao).select_related('cavalo').order_by('cavalo', '-valor')
    
    # Agrupar por cavalo e pegar o último lance de cada
    cavalos_dict = {}
    for lance in lances:
        if lance.cavalo.id not in cavalos_dict:
            # Adicionar atributo diretamente no objeto cavalo
            lance.cavalo.ultimo_lance_valor = lance.valor
            cavalos_dict[lance.cavalo.id] = lance.cavalo
    
    cavalos_com_lances = list(cavalos_dict.values())
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Detalhes do Leilão',
        'page_subtitle': leilao.nome,
        'page_icon': 'icofont icofont-gavel',
        'leilao': leilao,
        'cavalos_com_lances': cavalos_com_lances,
    }
    
    return render(request, 'backend/leilao_detalhe.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def leilao_form(request, id=None):
    leilao = None
    if id:
        leilao = get_object_or_404(Leilao, pk=id)
    if request.method == 'POST':
        if id:
            imagem_antiga = leilao.imagem.path if leilao and leilao.imagem else None
            form = LeilaoForm(request.POST, request.FILES, instance=leilao)
            if form.is_valid():
                if 'imagem' in request.FILES and imagem_antiga:
                    if os.path.isfile(imagem_antiga):
                        os.remove(imagem_antiga)
                leilao = form.save(commit=False)
                leilao.save()
                return redirect('leilao:leilao_detalhe', id=leilao.pk)
        else:
            # CORRIGIDO: adicionar request.FILES
            form = LeilaoForm(request.POST, request.FILES)
            if form.is_valid():
                leilao = form.save(commit=False)
                leilao.save()
                return redirect('leilao:leilao_detalhe', id=leilao.pk)
        page_subtitle = 'Editar Leilão' if id else 'Adicionar Leilão'
    else:
        form = LeilaoForm(instance=leilao) if id else LeilaoForm()
        page_subtitle = 'Editar Leilão' if id else 'Adicionar Leilão'

    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Leilão',
        'page_subtitle': page_subtitle,
        'page_icon': 'icofont icofont-court-hammer',
        'form': form,
        'leilao': leilao,
    }
    return render(request, 'backend/leilao_form.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def leilao_excluir(request, id):
    leilao = get_object_or_404(Leilao, pk=id)
    if request.method == 'POST':
        leilao.delete()
        return redirect('leilao:leilao_lista')