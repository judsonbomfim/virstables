from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
        
    # URLs do Frontend (para clientes)
    path('', include('apps.home.urls_frontend', namespace='home_frontend')),
    path('leilao/', include('apps.leilao.urls_frontend', namespace='leilao_frontend')),
    path('cavalo/', include('apps.cavalo.urls_frontend', namespace='cavalo_frontend')),
    path('', include('apps.users.urls_frontend', namespace='users_frontend')),
    path('opiniao/', include('apps.blog.urls_frontend', namespace='blog_frontend')),

    # URLs do Backend (painel administrativo personalizado)
    path('painel/', include('apps.home.urls_backend', namespace='home_backend')),
    path('painel/leilao/', include('apps.leilao.urls_backend', namespace='leilao_backend')),
    path('painel/cavalo/', include('apps.cavalo.urls_backend', namespace='cavalo_backend')),
    path('painel/emails/', include('apps.emails.urls_backend', namespace='emails_backend')),
    path('painel/site_config/', include('apps.site_config.urls_backend', namespace='site_config_backend')),
    path('painel/opiniao/', include('apps.blog.urls_backend', namespace='blog_backend')),
    path('painel/users/', include('apps.users.urls_backend', namespace='users_backend')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)