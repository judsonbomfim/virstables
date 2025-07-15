from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
        
    # URLs do Frontend (para clientes)
    path('', include('apps.home.urls_frontend', namespace='home_frontend')),
    path('', include('apps.leilao.urls_frontend', namespace='leilao_frontend')),
    path('', include('apps.cavalo.urls_frontend', namespace='cavalo_frontend')),
    path('', include('apps.users.urls_frontend', namespace='users_frontend')),

    # URLs do Backend (painel administrativo personalizado)
    path('painel/', include('apps.home.urls_backend', namespace='home_backend')),
    path('painel/', include('apps.leilao.urls_backend', namespace='leilao_backend')),
    path('painel/', include('apps.cavalo.urls_backend', namespace='cavalo_backend')),    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)