from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import JsonResponse
from apps.cavalo.models import Cavalo
from apps.leilao.models import Leilao, Lance

# Create your views here.
@login_required(login_url='/login/')
def index(request):    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Home',
    }
    
    return render(request, 'backend/index.html', context)

def cavalo_detalhe(request, slug):
    cavalo = Cavalo.objects.get(slug=slug)
    leilao = Leilao.objects.filter(cavalos_leilao=cavalo).first()  # ou ajuste conforme sua relação

    ultimo_lance = None
    if leilao:
        # ultimo_lance = leilao.lance_leilao.order_by('-data').first()
        ultimo_lance = Lance.objects.filter(cavalo=cavalo).order_by('-valor', '-data').first()

    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Detalhes do Cavalo: {cavalo.nome}',
        'cavalo': cavalo,
        'leilao': leilao,
        'ultimo_lance': ultimo_lance,
    }
    return render(request, 'frontend/cavalo_detalhe.html', context)


@login_required(login_url='/login/')
def dar_lance(request, cavalo_id):
    print(f">>>>>> Método: {request.method}")
    print(f">>>>>> Cavalo ID: {cavalo_id}")
    
    cavalo = get_object_or_404(Cavalo, id=cavalo_id)
    
    if request.method == 'POST':
        print(">>>>>> Lance iniciado")
        print(f">>>>>> POST data: {request.POST}")
        valor = request.POST.get('valor')
        
        try:
            from decimal import Decimal
            from django.core.exceptions import ValidationError
            
            lance = Lance(
                cavalo=cavalo,
                leilao=cavalo.leilao,
                usuario=request.user,
                valor=Decimal(valor)
            )
            lance.clean()  # Valida as regras de negócio
            lance.save()
            
            print(f">>>>>> Lance salvo com sucesso: R$ {valor}")
            messages.success(request, f'Lance de R$ {valor} realizado com sucesso!')
            
        except ValidationError as e:
            # Captura especificamente erros de validação
            # CORREÇÃO: Extrair a mensagem sem colchetes
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