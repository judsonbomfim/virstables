from django.urls import path
from .views import backend

app_name = 'home'

urlpatterns = [
    # frontend
    path('', backend.index, name='home'),
]