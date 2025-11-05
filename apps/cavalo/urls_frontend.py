from django.urls import path
from .views import frontend

app_name = 'cavalo'

urlpatterns = [
    path('venda-permanente/', frontend.venda_permanente, name='venda_permanente'),
    path('<slug:slug>/', frontend.cavalo_detalhe, name='cavalo_detalhe'),
    path('lance/<int:cavalo_id>/', frontend.dar_lance, name='dar_lance'),
]