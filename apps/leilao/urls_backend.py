from django.urls import path
from .views import backend

app_name = 'leilao'

urlpatterns = [
    path('', backend.leilao_lista, name='leilao_lista'),
    path('adicionar/', backend.leilao_form, name='leilao_adicionar'),
    path('editar/<int:id>/', backend.leilao_form, name='leilao_editar'),
    path('detalhe/<int:id>/', backend.leilao_detalhe, name='leilao_detalhe'),
    path('excluir/<int:id>/', backend.leilao_excluir, name='leilao_excluir'),
]