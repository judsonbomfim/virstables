from django.urls import path
from .views import frontend

app_name = 'leilao_frontend'

urlpatterns = [
    # lista
    path('', frontend.leilao_lista, name='leilao_lista'),
    path('leilao/<slug:slug>/', frontend.leilao_detalhe, name='leilao_detalhe'),
]