from django.urls import path
from . import views

app_name = 'site_config_backend'

urlpatterns = [
    path('', views.site_config_detalhes, name='site_config_detalhes'),
    path('configuracoes/<int:pk>/edit/', views.site_settings_edit, name='site_settings_edit'),
    path('banner/add/', views.banner_add, name='banner_add'),
    path('banner/<int:pk>/edit/', views.banner_edit, name='banner_edit'),
    path('banner/<int:pk>/delete/', views.banner_delete, name='banner_delete'),
    path('logo/add/', views.logo_add, name='logo_add'),
    path('logo/<int:pk>/edit/', views.logo_edit, name='logo_edit'),
    path('logo/<int:pk>/delete/', views.logo_delete, name='logo_delete'),
]