from django.urls import path
from .views import frontend
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    # Adicione suas rotas aqui
    path('cadastro/', frontend.cadastro, name='cadastro'),
    path('login/', frontend.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home_frontend:home'), name='logout'),
]