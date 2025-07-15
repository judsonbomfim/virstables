from django.urls import path
from .views import frontend

app_name = 'leilao'

urlpatterns = [
    path('leilao/', frontend.leilao_detalhe, name='leilao_detalhe'),
    path('leilao/<slug:slug>/', frontend.leilao_detalhe, name='leilao_detalhe'),    
]