from django.urls import path
from .views import frontend

app_name = 'home'

urlpatterns = [
    # frontend
    path('home', frontend.home, name='home'),
    path('', frontend.home_breve, name='home_breve'),
]