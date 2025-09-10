from django.urls import path
from .views import frontend

app_name = 'leilao'

urlpatterns = [
    path('', frontend.leilao_detalhe, name='leilao_detalhe'),
    path('<slug:slug>/', frontend.leilao_detalhe, name='leilao_detalhe'),    
]