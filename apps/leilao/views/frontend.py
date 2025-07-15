from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.leilao.models import Leilao
from django.utils import timezone
import pytz

def data_atual():
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora = timezone.now().astimezone(fuso_br)
    return agora.replace(tzinfo=None)

# Create your views here.
# @login_required(login_url='/login/')
def index(request):
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Home',
    }    
    return render(request, 'backend/index.html', context)


def leilao_detalhe(request, slug):
    leilao = Leilao.objects.get(slug=slug)
    cavalos = leilao.cavalos_leilao.all()
    
    hoje = data_atual()
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Leilão: {leilao.nome}',
        'data_hoje': hoje,
        'leilao': leilao,
        'cavalos': cavalos,
    }
    return render(request, 'frontend/leilao_detalhe.html', context)