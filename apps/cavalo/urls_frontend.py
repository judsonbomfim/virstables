from django.urls import path
from .views import frontend

app_name = 'cavalo'

urlpatterns = [
    path('cavalo/<slug:slug>/', frontend.cavalo_detalhe, name='cavalo_detalhe'),
]