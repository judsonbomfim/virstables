from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.leilao.models import Leilao, Lance
from django.utils import timezone
import pytz

def data_atual():
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora = timezone.now().astimezone(fuso_br)
    return agora.replace(tzinfo=None)

# Create your views here.
# @login_required(login_url='/login/')

def leilao_detalhe(request, slug):
    leilao = Leilao.objects.get(slug=slug)
    cavalos = leilao.cavalos_leilao.all()
    
    # Buscar o último lance para cada cavalo
    cavalos_com_lances = []
    for cavalo in cavalos:
        ultimo_lance = Lance.objects.filter(cavalo=cavalo).order_by('-valor', '-data').first()
        cavalos_com_lances.append({
            'cavalo': cavalo,
            'ultimo_lance': ultimo_lance
        })
    
    hoje = data_atual()
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Leilão: {leilao.nome}',
        'data_hoje': hoje,
        'leilao': leilao,
        'cavalos_com_lances': cavalos_com_lances,  # Nova variável
    }
    return render(request, 'frontend/leilao_detalhe.html', context)