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
def home(request):
    
    leiloes = Leilao.objects.all().order_by('-data_inicio').filter(status='ativo')
    hoje = data_atual()
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Home',
        'leiloes': leiloes,
        'data_hoje': hoje,
    }
    return render(request, 'frontend/index.html', context)