from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import JsonResponse
from apps.cavalo.models import Cavalo
from apps.emails.tasks import email_lance_coberto, email_lance_confirmado
from apps.leilao.models import Leilao, Lance
from apps.cavalo.classes import exibirLance

# Create your views here.
def index(request):    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Home',
    }
    
    return render(request, 'backend/index.html', context)

def cavalo_detalhe(request, slug):
    
    from apps.site_config.models import SiteSettings
    site = SiteSettings.objects.first()
    
    cavalo = Cavalo.objects.get(slug=slug)
    leilao = Leilao.objects.filter(cavalos_leilao=cavalo).first()  # ou ajuste conforme sua relação

    ultimo_lance = None
    exibir_lance = 'n'
    if leilao:
        # ultimo_lance = leilao.lance_leilao.order_by('-data').first()
        ultimo_lance = Lance.objects.filter(cavalo=cavalo).order_by('-valor', '-data').first()

        exibir_lance = exibirLance(leilao.id)

    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Detalhes do Cavalo: {cavalo.nome}',
        'cavalo': cavalo,
        'leilao': leilao,
        'ultimo_lance': ultimo_lance,
        'site': site,
        'exibir_lance': exibir_lance,
    }
    return render(request, 'frontend/cavalo_detalhe.html', context)

def venda_permanente(request):
    from apps.site_config.models import SiteSettings
    site = SiteSettings.objects.first()
    
    cavalos = Cavalo.objects.filter(leilao__isnull=True).order_by('-data_cadastro')
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Cavalos à Venda Permanente',
        'cavalos': cavalos,
        'site': site,
    }
    return render(request, 'frontend/cavalo_venda_permanente.html', context)

@login_required(login_url='/login/')
def dar_lance(request, cavalo_id):
    
    cavalo = get_object_or_404(Cavalo, id=cavalo_id)
    
    if request.method == 'POST':
        print(">>>>>> Lance iniciado")
        print(f">>>>>> POST data: {request.POST}")
        valor = request.POST.get('valor')
        
        try:
            from decimal import Decimal
            from django.core.exceptions import ValidationError
            
            lance_anterior = Lance.objects.filter(cavalo=cavalo).order_by('-data').first()
            
            # CORREÇÃO: Verificar se lance_anterior existe ANTES de acessar .usuario
            if lance_anterior and lance_anterior.usuario.id != request.user.id:
                email_lance_coberto.delay(lance_anterior.id)
            
            lance = Lance(
                cavalo=cavalo,
                leilao=cavalo.leilao,
                usuario=request.user,
                valor=Decimal(valor)
            )
            lance.clean()  # Valida as regras de negócio
            lance.save()

            email_lance_confirmado.delay(lance.id)

            print(f">>>>>> Lance salvo com sucesso: R$ {valor}")
            messages.success(request, f'Lance de R$ {valor} realizado com sucesso!')
            
        except ValidationError as e:
            # Captura especificamente erros de validação
            if hasattr(e, 'messages') and e.messages:
                error_message = e.messages[0]  # Pega a primeira mensagem
            else:
                error_message = str(e)
            
            print(f">>>>>> Erro de validação: {error_message}")
            messages.error(request, error_message)
            
        except Exception as e:
            # Captura outros erros
            print(f">>>>>> Erro geral: {str(e)}")
            messages.error(request, f'Erro ao dar lance: {str(e)}')
    
    return redirect('cavalo_frontend:cavalo_detalhe', slug=cavalo.slug)