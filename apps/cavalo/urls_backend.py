from django.urls import path
from .views import backend

app_name = 'cavalo'

urlpatterns = [
    path('cavalo/listar/', backend.cavalo_lista, name='cavalo_lista'),
    path('cavalo/adicionar/', backend.cavalo_form, name='cavalo_adicionar'),
    path('cavalo/adicionar/<int:id_leilao>/', backend.cavalo_form, name='cavalo_adicionar_leilao'),
    path('cavalo/adicionar/video/<int:id>/', backend.cavalo_form_video, name='cavalo_video_adicionar'),
    path('cavalo/adicionar/foto/<int:id>/', backend.cavalo_form_foto, name='cavalo_foto_adicionar'),
    path('cavalo/adicionar/foto/', backend.cavalo_form_foto, name='cavalo_foto_upload'),
    path('cavalo/detalhe/<int:id>/', backend.cavalo_detalhe, name='cavalo_detalhe'),
    path('cavalo/editar/<int:id_cavalo>/', backend.cavalo_form, name='cavalo_editar'),
    path('cavalo/excluir/video/<int:id>/', backend.cavalo_video_excluir, name='cavalo_video_excluir'),
    path('cavalo/excluir/foto/<int:id>/', backend.cavalo_foto_excluir, name='cavalo_foto_excluir'),
]