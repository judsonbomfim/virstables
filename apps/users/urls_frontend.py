from django.urls import path
from django.contrib.auth import views as auth_views
from .views.frontend import (
    cadastro, 
    CustomLoginView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

app_name = 'users_frontend'

urlpatterns = [
    # Cadastro e Login
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home_frontend:home'), name='logout'),
    
    # Recuperação de senha
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]