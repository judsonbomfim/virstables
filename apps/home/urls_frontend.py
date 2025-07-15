from django.urls import path
from .views import frontend

app_name = 'home'

urlpatterns = [
    # frontend
    path('', frontend.home, name='home'),
]