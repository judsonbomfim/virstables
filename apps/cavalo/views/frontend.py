from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.cavalo.models import Cavalo
from apps.leilao.models import Leilao

# Create your views here.
# @login_required(login_url='/login/')
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
        ultimo_lance = leilao.lance_leilao.order_by('-data').first()

    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Detalhes do Cavalo: {cavalo.nome}',
        'cavalo': cavalo,
        'leilao': leilao,
        'ultimo_lance': ultimo_lance,
    }
    return render(request, 'frontend/cavalo_detalhe.html', context)
