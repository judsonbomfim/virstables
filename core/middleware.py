from django.shortcuts import redirect
from django.conf import settings

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