from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from .services import GoogleAnalyticsService
import json


@staff_member_required
def analytics_dashboard(request):
    """Dashboard principal de analytics"""
    try:
        ga = GoogleAnalyticsService()
        
        # Estatísticas gerais
        stats = ga.get_overview_stats(days=30)
        
        # Visitantes diários (para gráfico)
        daily_data = ga.get_daily_visitors(days=30)
        
        # Páginas mais visitadas
        top_pages = ga.get_top_pages(limit=10)
        
        # Fontes de tráfego
        traffic_sources = ga.get_traffic_sources()
        
        # Usuários em tempo real
        realtime_users = ga.get_realtime_users()
        
        # Cavalos mais visualizados
        top_cavalos = ga.get_top_cavalos(limit=10)
        
        context = {
            'painel_title': settings.PAINEL_TITLE,
            'page_title': 'Analytics Dashboard',
            'page_icon': 'icofont icofont-spreadsheet',
            'pagesub_title': 'Analytics Dashboard',
            'stats': stats,
            'daily_data_json': json.dumps(daily_data),
            'top_pages': top_pages,
            'traffic_sources': traffic_sources,
            'realtime_users': realtime_users,
            'top_cavalos': top_cavalos,
        }
        
        return render(request, 'analytics/dashboard.html', context)
        
    except Exception as e:
        context = {
            'error': str(e),
        }
        return render(request, 'analytics/dashboard.html', context)


@staff_member_required
def cavalos_analytics(request):
    """Relatório completo de analytics de cavalos"""
    try:
        ga = GoogleAnalyticsService()
        
        # Comparação de cavalos
        cavalos_comparison = ga.get_cavalos_comparison(days=30)
        
        context = {
            'cavalos': cavalos_comparison,
        }
        
        return render(request, 'analytics/cavalos.html', context)
        
    except Exception as e:
        context = {
            'error': str(e),
        }
        return render(request, 'analytics/cavalos.html', context)


@staff_member_required
def cavalo_detail_analytics(request, cavalo_id):
    """Analytics detalhado de um cavalo específico"""
    try:
        # REMOVER IMPORT DAQUI - importar no topo do arquivo se necessário
        # Ou fazer import dinâmico se for opcional
        try:
            from apps.cavalo.models import Cavalo
            cavalo = get_object_or_404(Cavalo, id=cavalo_id)
        except ImportError:
            # Se o app cavalos não existir, use dados genéricos
            cavalo = None
        
        ga = GoogleAnalyticsService()
        
        # Estatísticas do cavalo
        cavalo_slug = cavalo.slug if cavalo and hasattr(cavalo, 'slug') else cavalo_id
        stats = ga.get_cavalo_stats(cavalo_slug)
        
        context = {
            'cavalo': cavalo,
            'cavalo_id': cavalo_id,
            'stats_json': json.dumps(stats),
        }
        
        return render(request, 'analytics/cavalo_detail.html', context)
        
    except Exception as e:
        context = {
            'error': str(e),
        }
        return render(request, 'analytics/cavalo_detail.html', context)