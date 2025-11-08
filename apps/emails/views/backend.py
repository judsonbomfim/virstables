from django.conf import settings
from django.shortcuts import render

from apps.emails.tasks import email_lance_confirmado


# def viewEmail(request, email_id):
    
#     email_lance_confirmado.delay(email_id)
    
#     context = {
#         'url_site': 'https://www.virtualstables.com.br/',
#         'title_email': "Lance Confirmado",
#         'primeiro_nome': 'Judson',
#         'valor_lance': 'R$ 100,00',
#         'cavalo': 'TEMPLARIO VP',
#     }
#     return render(request, 'partials/lance_confirmado.html', context)