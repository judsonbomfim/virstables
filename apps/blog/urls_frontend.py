from django.urls import path
from .views import frontend

app_name = 'blog'

urlpatterns = [
    path('', frontend.post_list, name='post_home'),
    path('<slug:slug>/', frontend.post_detalhe, name='post_detalhe'),
]