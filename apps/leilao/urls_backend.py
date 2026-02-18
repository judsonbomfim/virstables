from django.urls import path
from .views import backend

app_name = 'leilao'

urlpatterns = [
    path('leilao/', backend.leilao_lista, name='leilao_lista'),
    path('leilao/adicionar/', backend.leilao_form, name='leilao_adicionar'),
    path('leilao/editar/<int:id>/', backend.leilao_form, name='leilao_editar'),
    path('leilao/detalhe/<int:id>/', backend.leilao_detalhe, name='leilao_detalhe'),
    path('leilao/excluir/<int:id>/', backend.leilao_excluir, name='leilao_excluir'),
]