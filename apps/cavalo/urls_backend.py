from django.urls import path
from .views import backend

app_name = 'cavalo'

urlpatterns = [
    path('listar/', backend.cavalo_lista, name='cavalo_lista'),
    path('adicionar/', backend.cavalo_form, name='cavalo_adicionar'),
    path('adicionar/<int:id_leilao>/', backend.cavalo_form, name='cavalo_adicionar_leilao'),
    path('adicionar/video/<int:id>/', backend.cavalo_form_video, name='cavalo_video_adicionar'),
    path('adicionar/foto/<int:id>/', backend.cavalo_form_foto, name='cavalo_foto_adicionar'),
    path('adicionar/foto/', backend.cavalo_form_foto, name='cavalo_foto_upload'),
    path('detalhe/<int:id>/', backend.cavalo_detalhe, name='cavalo_detalhe'),
    path('editar/<int:id_cavalo>/', backend.cavalo_form, name='cavalo_editar'),
    path('editar/<int:id_cavalo>/', backend.cavalo_form, name='cavalo_editar'),
    path('excluir/<int:id>/', backend.cavalo_excluir, name='cavalo_excluir'),
    path('excluir/video/<int:id>/', backend.cavalo_video_excluir, name='cavalo_video_excluir'),
    path('excluir/foto/<int:id>/', backend.cavalo_foto_excluir, name='cavalo_foto_excluir'),
]