from django.shortcuts import redirect
from django.conf import settings


class SubdomainMiddleware:
    """
    Detecta requisições vindas do subdomínio 'app.' e marca
    request.is_app_subdomain = True para suprimir header/footer.
    O subdomínio é configurável via settings.APP_SUBDOMAIN_PREFIX (padrão: 'app').
    Remove o header X-Frame-Options para permitir embedding via WebView/iframe (FlutterFlow).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.prefix = getattr(settings, 'APP_SUBDOMAIN_PREFIX', 'app')

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        request.is_app_subdomain = host.startswith(f'{self.prefix}.')
        response = self.get_response(request)
        if request.is_app_subdomain:
            response.headers.pop('X-Frame-Options', None)
        return response

class MaintenanceMiddleware:
    """
    Middleware para colocar site em manutenção.
    Ativa/desativa via settings.MAINTENANCE_MODE
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que sempre ficam acessíveis
        exempt_urls = [
            '/login/',
            '/logout/',
            '/admin/',
            '/static/',
            '/media/',
        ]
        
        # Verifica se modo manutenção está ativo
        maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)
        
        if maintenance_mode and not request.user.is_authenticated:
            # Permite acesso apenas às URLs isentas
            if not any(request.path.startswith(url) for url in exempt_urls):
                return redirect(f'/login/?next={request.path}')
        
        response = self.get_response(request)
        return response