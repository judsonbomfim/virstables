from django.urls import path
from .views import frontend

app_name = 'cavalo'

urlpatterns = [
    path('cavalo/<slug:slug>/', frontend.cavalo_detalhe, name='cavalo_detalhe'),
    path('cavalo/lance/<int:cavalo_id>/', frontend.dar_lance, name='dar_lance'),
]