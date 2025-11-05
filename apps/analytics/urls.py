from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    path('cavalos/', views.cavalos_analytics, name='cavalos'),
    path('cavalo/<int:cavalo_id>/', views.cavalo_detail_analytics, name='cavalo_detail'),
]