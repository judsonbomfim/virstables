from urllib import request
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from apps.emails.classes import send_email
from apps.leilao.models import Lance
from apps.users.models import PerfilCliente


@shared_task
def email_cadastro_analise(id):

    cliente = PerfilCliente.objects.get(pk=id) if id else None
    nome_cliente = cliente.nome_completo if cliente else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = cliente.usuario.email if cliente else settings.DEFAULT_FROM_EMAIL
    title_email = "Confirmação em Análise"

    context = {
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome
    }
    html_content = render_to_string('partials/cadastro_analise.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email} - {nome_cliente}" if cliente else title_email
    # Enviar E-mail
    send_email(html_content, text_content, subject, [email_cliente])

@shared_task
def email_cadastro_confirmado(id):

    cliente = PerfilCliente.objects.get(pk=id) if id else None
    nome_cliente = cliente.nome_completo if cliente else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = cliente.usuario.email if cliente else settings.DEFAULT_FROM_EMAIL
    title_email = "Confirmação de Cadastro"
    
    context = {
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome
    }
    html_content = render_to_string('partials/cadastro_confirmado.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email} - {nome_cliente}" if cliente else title_email
    # Enviar E-mail
    send_email(html_content, text_content, subject, [email_cliente])

@shared_task
def email_lance_confirmado(id):

    print(">>>>> Enviando email de lance confirmado")
    lance = Lance.objects.get(pk=id) if id else None
    cliente = lance.usuario.perfil_cliente if lance and hasattr(lance.usuario, 'perfil_cliente') else None
    cavalo = lance.cavalo if lance else "Cavalo Desconhecido"
    valor_lance = lance.valor if lance else "R$ 0,00"
    nome_cliente = cliente.nome_completo if lance and hasattr(lance.usuario, 'perfil_cliente') else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = lance.usuario.email if lance else settings.DEFAULT_FROM_EMAIL
    title_email = "Lance Confirmado"
    
    context = {
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome,
        'valor_lance': valor_lance,
        'cavalo': cavalo,
    }
    html_content = render_to_string('partials/lance_confirmado.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email} - {nome_cliente}" if cliente else title_email
    # Enviar E-mail
    send_email(html_content, text_content, subject, [email_cliente])

@shared_task
def email_lance_coberto(id):

    lance = Lance.objects.get(pk=id) if id else None
    cliente = lance.usuario.perfil_cliente if lance and hasattr(lance.usuario, 'perfil_cliente') else None
    cavalo = lance.cavalo if lance else "Cavalo Desconhecido"
    valor_lance = lance.valor if lance else "R$ 0,00"
    nome_cliente = cliente.nome_completo if lance and hasattr(lance.usuario, 'perfil_cliente') else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = lance.usuario.email if lance else settings.DEFAULT_FROM_EMAIL
    title_email = "Lance Coberto"

    context = {
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome,
        'valor_lance': valor_lance,
        'cavalo': cavalo,
    }
    html_content = render_to_string('partials/lance_coberto.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email} - {nome_cliente}" if cliente else title_email
    # Enviar E-mail
    send_email(html_content, text_content, subject, [email_cliente])