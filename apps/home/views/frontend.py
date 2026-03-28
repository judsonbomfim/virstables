import pytz
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.blog.models import Post
from apps.leilao.models import Leilao
from django.utils import timezone
from apps.site_config.models import SiteSettings, Banner, Logo

def data_atual():
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora = timezone.now().astimezone(fuso_br)
    return agora.replace(tzinfo=None)

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    site_settings = SiteSettings.objects.first()
    banners = Banner.objects.order_by('ordem')
    logos = Logo.objects.order_by('ordem')
    
    leiloes = Leilao.objects.all().order_by('-data_inicio').filter(status='ativo')
    posts = Post.objects.all().order_by('-created_at')[:3]
    hoje = data_atual()
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Home',
        'site_settings': site_settings,
        'banners': banners,
        'logos': logos,
        'leiloes': leiloes,
        'posts': posts,
        'data_hoje': hoje,
    }
    return render(request, 'frontend/index.html', context)

# def home_breve(request):
    
#     leiloes = Leilao.objects.all().order_by('-data_inicio').filter(status='ativo')  # type: ignore
#     hoje = data_atual()
#     link_leilao = "https://www.leilonorte.com/web/evento/1153/8-leilao-virtual-ares-lusitanos-selecao"
#     context = {
#         'painel_title': settings.PAINEL_TITLE,
#         'page_title': 'Home',
#         'leiloes': leiloes,
#         'data_hoje': hoje,
#         'link_leilao': link_leilao,
#     }
#     return render(request, 'frontend/home_breve.html', context)