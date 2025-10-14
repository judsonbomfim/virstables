from io import BytesIO
import unicodedata
from PIL import Image
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.decorators import group_required
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib import messages
from django.db.models import Max  # Adicionada a importação do Max
from django.shortcuts import get_object_or_404, render, redirect
from apps.leilao.models import Leilao, Lance
from apps.cavalo.models import Cavalo, Video, Foto
from apps.cavalo.forms import CavaloForm, FotoForm, VideoForm


def youtube_to_embed(url):
    import re
    # Tenta pegar o ID do vídeo em diferentes formatos
    patterns = [
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    return url  # retorna original se não encontrar padrão

def remover_acentos_espacos(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome = nome.replace(' ', '_')
    return ''.join(c for c in nome if c.isalnum() or c in '._-')

@login_required(login_url='/login/')
@group_required('Administradores')
def cavalo_lista(request):

    cavalos = Cavalo.objects.filter(leilao__isnull=True)
    print(f"Total de cavalos disponíveis: {cavalos.count()}")  # Debugging line
    page_title = 'Cavalos Individuais Disponíveis'
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': page_title,
        'page_icon': 'icofont icofont-animal-horse-head-alt-1',
        'pagesub_title': 'Cavalos Disponíveis',
        'cavalos': cavalos,
    }
    
    return render(request, 'backend/cavalo_lista.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def cavalo_detalhe(request, id):

    cavalo = get_object_or_404(Cavalo, pk=id)
    leilao_nome = cavalo.leilao.nome if cavalo.leilao else ""
    fotos = Foto.objects.filter(cavalo=cavalo).order_by('ordem')
    videos = Video.objects.filter(cavalo=cavalo).order_by('-id')
    #Listar os lances deste cavalo especificamente
    if cavalo.leilao:
        lances = Lance.objects.filter(cavalo=cavalo).order_by('-valor')
    else:
        lances = None

    if request.method == 'POST':
        if 'foto_id' in request.POST and 'is_destaque' in request.POST:
            # Atualizar o destaque
            try:
                foto_id = request.POST.get('foto_id')
                is_destaque = request.POST.get('is_destaque') == 'true'
                foto = get_object_or_404(Foto, id=foto_id, cavalo=cavalo)
                foto.is_destaque = is_destaque
                foto.save()  # O método save desmarca outras fotos
                messages.success(request, 'Foto de destaque atualizado com sucesso!')
                return JsonResponse({'status': 'ok', 'redirect_url': request.path})
            except Exception as e:
                messages.error(request, f'Erro ao atualizar destaque: {str(e)}')
                return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=500)
        
        if 'ordem[]' in request.POST:
            # Processar a reordenação
            try:
                novos_ordens = request.POST.getlist('ordem[]')
                for index, foto_id in enumerate(novos_ordens, start=1):
                    Foto.objects.filter(id=foto_id, cavalo=cavalo).update(ordem=index)
                messages.success(request, 'Ordem das fotos atualizada com sucesso!')
                return JsonResponse({'status': 'ok', 'redirect_url': request.path})
            except Exception as e:
                messages.error(request, f'Erro ao atualizar ordem: {str(e)}')  # Adicionar mensagem de erro
                return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=500)

    # Listar fotos para exibição

    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Detalhes de {cavalo.nome}',
        'page_subtitle': 'Ordenar Fotos',
        'page_icon': 'icofont icofont-camera',
        'cavalo': cavalo,
        'leilao_nome': leilao_nome,
        'fotos': fotos,
        'videos': videos,
        'lances': lances,
    }
    return render(request, 'backend/cavalo_detalhe.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def cavalo_form(request, id_cavalo=None, id_leilao=None):
    
    cavalo = None
    leilao = None
    page_subtitle = ''
    if request.method == 'POST':
        if id_cavalo:
            print(">>> Editando cavalo com ID:", id_cavalo)  # Debug
            cavalo = Cavalo.objects.get(pk=id_cavalo)
            form = CavaloForm(request.POST, instance=cavalo)
            if form.is_valid():
                cavalo = form.save(commit=False)
                cavalo.save()
                return redirect('cavalo_backend:cavalo_detalhe', id=cavalo.pk)
            else:
                page_subtitle = 'Editar Leilão'
        else:
            print(">>> Adicionando novo cavalo")  # Debug
            if id_leilao:
                leilao = get_object_or_404(Leilao, pk=id_leilao)
            form = CavaloForm(request.POST)
            if form.is_valid():
                cavalo = form.save(commit=False)
                cavalo.save()
                if id_leilao:
                    return redirect('leilao_backend:leilao_detalhe', id=leilao.pk)
                else:
                    return redirect('cavalo_backend:cavalo_lista')
            else:
                page_subtitle = f'Adicionar Cavalo ao Leilão: {leilao.nome}' if id_leilao else 'Adicionar Cavalo'
    else:
        if id_cavalo:
            cavalo = Cavalo.objects.get(pk=id_cavalo)
            page_subtitle = 'Editar Leilão'
            form = CavaloForm(instance=cavalo)
        elif id_leilao:
            leilao = Leilao.objects.get(pk=id_leilao)
            page_subtitle = f'Adicionar Cavalo ao Leilão: {leilao.nome}'
            form = CavaloForm(initial={'leilao': leilao})
        else:
            form = CavaloForm()
            page_subtitle = 'Adicionar Cavalo'

    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Cavalo',
        'page_subtitle': page_subtitle,
        'page_icon': 'icofont icofont-animal-horse-head-alt-1',
        'form': form,
        'cavalo': cavalo,
        'leilao': leilao,
        'errors': form.errors if form.errors else None,
    }
    return render(request, 'backend/cavalo_form.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def cavalo_form_video(request,id):
            
    cavalo = get_object_or_404(Cavalo, pk=id)
    if cavalo.leilao:
        leilao_nome = cavalo.leilao.nome
    else:
        leilao_nome = ""

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            # Altere o campo desejado antes de salvar
            video.url_youtube = youtube_to_embed(video.url_youtube)
            video.cavalo = cavalo  # Garante que o cavalo está correto
            video.save()
            return redirect('cavalo_backend:cavalo_detalhe', id=cavalo.id)
        else:
            print("Erros do form:", form.errors)
    else:
        form = VideoForm(initial={'cavalo': cavalo})

    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Adicionar Vídeo para {cavalo.nome}',
        'page_subtitle': 'Adicionar Vídeo',
        'page_icon': 'icofont icofont-brand-youtube',
        'form': form,
        'cavalo': cavalo,
        'leilao_nome': leilao_nome,
    }

    return render(request, 'backend/cavalo_form video.html', context)


@login_required(login_url='/login/')
@group_required('Administradores')
def cavalo_form_foto(request, id=None):
        
    print(">>> Entrou na view cavalo_form_foto")
    cavalo = get_object_or_404(Cavalo, pk=id)
    leilao_nome = cavalo.leilao.nome if cavalo.leilao else ""

    if request.method == 'POST':
        cavalo_id = request.POST.get('cavalo_id') or id
        print(">>> cavalo_id recebido:", cavalo_id)
        cavalo = get_object_or_404(Cavalo, id=cavalo_id)
        arquivos = request.FILES.getlist('file')
        fotos_criadas = []

        if not arquivos:
            print(">>> Nenhum arquivo recebido")
            return JsonResponse({'status': 'erro', 'mensagem': 'Nenhum arquivo enviado'}, status=400)

        for arquivo in arquivos:
            print(">>> Processando arquivo:", arquivo.name)
            nome_base, ext = arquivo.name.rsplit('.', 1)
            nome_base = remover_acentos_espacos(nome_base)
            novo_nome = f"{nome_base}_{cavalo.id}.{ext.lower()}"

            try:
                img = Image.open(arquivo)
                if img.width > 1440:
                    proporcao = 1440 / float(img.width)
                    nova_altura = int(float(img.height) * proporcao)
                    img = img.resize((1440, nova_altura), Image.Resampling.LANCZOS)
                img_io = BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_io.seek(0)

                # Calcular a próxima ordem para o cavalo
                ultima_ordem = Foto.objects.filter(cavalo=cavalo).aggregate(Max('ordem'))['ordem__max'] or 0
                nova_ordem = ultima_ordem + 1

                # Incluir todos os campos obrigatórios no formulário
                data = {
                    'cavalo': cavalo.id,
                    'is_destaque': False,  # Definir como False por padrão
                    'ordem': nova_ordem,   # Definir a próxima ordem
                }
                files = {'imagem': ContentFile(img_io.read(), novo_nome)}

                form = FotoForm(data, files)
                print(">>> Dados do form:", data, files)
                if form.is_valid():
                    foto = form.save(commit=False)
                    foto.cavalo = cavalo
                    foto.save()
                    fotos_criadas.append(foto.id)
                    print(">>> Foto salva com ID:", foto.id)
                else:
                    print(">>> Formulário inválido:", form.errors)
                    return JsonResponse({'status': 'erro', 'erros': form.errors.as_json()}, status=400)
            except Exception as e:
                print(">>> Erro ao processar arquivo:", str(e))
                return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=500)

        return JsonResponse({'status': 'ok', 'fotos': fotos_criadas})

    else:
        form = FotoForm(initial={'cavalo': cavalo})

    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Adicionar Foto para {cavalo.nome}',
        'page_subtitle': 'Adicionar Foto',
        'page_icon': 'icofont icofont-camera',
        'form': form,
        'cavalo': cavalo,
        'leilao_nome': leilao_nome,
    }

    return render(request, 'backend/cavalo_form foto.html', context)


# ...existing code...
@login_required(login_url='/login/')
@group_required('Administradores')
def cavalo_excluir(request, id):
    cavalo = get_object_or_404(Cavalo, pk=id)
    if request.method == 'POST':
        from django.db import transaction
        import os
        try:
            with transaction.atomic():
                # Excluir fotos e arquivos físicos
                fotos = Foto.objects.filter(cavalo=cavalo)
                for foto in fotos:
                    try:
                        # Remove via storage (compatível com S3, etc.)
                        if foto.imagem:
                            caminho_local = foto.imagem.path if hasattr(foto.imagem, 'path') else None
                            foto.imagem.delete(save=False)
                            # (Opcional) garantir remoção local se ainda existir
                            if caminho_local and os.path.isfile(caminho_local):
                                try:
                                    os.remove(caminho_local)
                                except Exception:
                                    pass
                    except Exception as e:
                        messages.warning(request, f'Falha ao remover arquivo da foto {foto.id}: {e}')
                    foto.delete()

                # Excluir vídeos (não há arquivo físico, apenas registro)
                Video.objects.filter(cavalo=cavalo).delete()

                # Finalmente excluir o cavalo
                cavalo.delete()
                messages.success(request, 'Cavalo e mídias associadas excluídos com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir cavalo: {e}')
        return redirect('cavalo_backend:cavalo_lista')

@login_required(login_url='/login/')
@group_required('Administradores')
def cavalo_video_excluir(request, id):
    
    video = get_object_or_404(Video, pk=id)
    cavalo_id = video.cavalo_id
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Vídeo excluído com sucesso!')
    # Redirecionar para a página de detalhes do cavalo
    if cavalo_id:
        return redirect('cavalo_backend:cavalo_detalhe', cavalo_id)


@login_required(login_url='/login/')
@group_required('Administradores')
def cavalo_foto_excluir(request, id):
    
    foto = get_object_or_404(Foto, pk=id)
    cavalo_id = foto.cavalo_id
    if request.method == 'POST':
        # Excluir arquivo físico da foto
        if foto.imagem and foto.imagem.path:
            import os
            try:
                if os.path.isfile(foto.imagem.path):
                    os.remove(foto.imagem.path)
            except Exception as e:
                messages.error(request, f'Erro ao remover arquivo da foto: {str(e)}')
        foto.delete()
        messages.success(request, 'Foto excluída com sucesso!')
    # Redirecionar para a página de detalhes do cavalo
    if cavalo_id:
        return redirect('cavalo_backend:cavalo_detalhe', cavalo_id)