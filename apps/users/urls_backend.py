from django.urls import path
from .views import backend

app_name = 'users_backend'

urlpatterns = [
    path('clientes/', backend.cliente_lista, name='cliente_lista'),
    path('clientes/<int:id>/', backend.cliente_detalhe, name='cliente_detalhe'),
    path('clientes/<int:id>/editar/', backend.cliente_editar, name='cliente_editar'),
    path('clientes/<int:id>/aprovar/', backend.cliente_aprovar, name='cliente_aprovar'),
]