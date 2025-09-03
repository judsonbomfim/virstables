from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives



def send_email(html_content, text_content, subject, email_cliente):

    email = EmailMultiAlternatives(
        #subject
        subject,
        #content
        text_content,
        #from email
        f"{settings.PAINEL_TITLE} <{settings.DEFAULT_FROM_EMAIL}>",
        #to
        [email_cliente] if isinstance(email_cliente, str) else email_cliente,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()