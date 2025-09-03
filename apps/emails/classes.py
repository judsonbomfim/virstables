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
        settings.DEFAULT_FROM_EMAIL,
        f"{settings.PAINEL_TITLE} <{settings.DEFAULT_FROM_EMAIL}>",
        #to
        [email_cliente],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()