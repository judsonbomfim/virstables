from django.urls import path
from .views import backend

app_name = 'emails'

urlpatterns = [
    path('email/view/int/<int:id>/', backend.viewEmail, name='email_view'),
]