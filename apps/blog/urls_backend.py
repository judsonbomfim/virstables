from django.urls import path
from .views import backend 

app_name = 'blog'

urlpatterns = [
    path('', backend.post_lista, name='post_lista'),
    path('novo/', backend.post_adicionar, name='post_adicionar'),
    path('<int:pk>/editar/', backend.post_editar, name='post_editar'),
    path('<int:pk>/excluir/', backend.post_delete, name='post_delete'),
    path('<slug:slug>/', backend.post_detalhe, name='post_detalhe'),
]