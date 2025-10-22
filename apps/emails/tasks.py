from urllib import request
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from apps.leilao.models import Lance
from apps.users.models import PerfilCliente


@shared_task
def email_cadastro_analise(id):

    cliente = PerfilCliente.objects.get(pk=id) if id else None
    nome_cliente = cliente.nome_completo if cliente else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = cliente.username.email if cliente else settings.DEFAULT_FROM_EMAIL

    context = {
        'url_site': 'https://www.virtualstables.com.br/',
        'title_email': "Confirmação de Cadastro",
        'primeiro_nome': primeiro_nome
    }
    html_content = render_to_string('partials/cadastro_analise.html', context)
    text_content = strip_tags(html_content)
    subject = f"Cadastro em Análise - {nome_cliente}" if cliente else "Cadastro em Análise"
    email = EmailMultiAlternatives(
        #subject
        subject,
        #content
        text_content,
        #from email
        settings.DEFAULT_FROM_EMAIL,
        #to
        [email_cliente],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

@shared_task
def email_cadastro_confirmado(id):

    cliente = PerfilCliente.objects.get(pk=id) if id else None
    nome_cliente = cliente.nome_completo if cliente else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = cliente.username.email if cliente else settings.DEFAULT_FROM_EMAIL

    context = {
        'url_site': 'https://www.virtualstables.com.br/',
        'title_email': "Confirmação de Cadastro",
        'primeiro_nome': primeiro_nome
    }
    html_content = render_to_string('partials/cadastro_confirmado.html', context)
    text_content = strip_tags(html_content)
    subject = f"Confirmação de Cadastro - {nome_cliente}" if cliente else "Confirmação de Cadastro"
    email = EmailMultiAlternatives(
        #subject
        subject,
        #content
        text_content,
        #from email
        settings.DEFAULT_FROM_EMAIL,
        #to
        [email_cliente],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

@shared_task
def email_lance_confirmado(id):

    print(">>>>>> Enviando email de lance confirmado")
    lance = Lance.objects.get(pk=id) if id else None
    cliente = lance.usuario.perfil_cliente if lance and hasattr(lance.usuario, 'perfil_cliente') else None
    cavalo = lance.cavalo if lance else "Cavalo Desconhecido"
    valor_lance = lance.valor if lance else "R$ 0,00"
    nome_cliente = lance.usuario.perfil_cliente.nome_completo if lance and hasattr(lance.usuario, 'perfil_cliente') else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = cliente.username.email if cliente else settings.DEFAULT_FROM_EMAIL

    context = {
        'url_site': 'https://www.virtualstables.com.br/',
        'title_email': "Lance Confirmado",
        'primeiro_nome': primeiro_nome,
        'valor_lance': valor_lance,
        'cavalo': cavalo,
    }
    html_content = render_to_string('partials/lance_confirmado.html', context)
    text_content = strip_tags(html_content)
    subject = f"Lance Confirmado - {nome_cliente}" if cliente else "Lance Confirmado"
    email = EmailMultiAlternatives(
        #subject
        subject,
        #content
        text_content,
        #from email
        settings.DEFAULT_FROM_EMAIL,
        #to
        [email_cliente],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

@shared_task
def email_lance_coberto(id):

    lance = Lance.objects.get(pk=id) if id else None
    cliente = lance.usuario.perfil_cliente if lance and hasattr(lance.usuario, 'perfil_cliente') else None
    cavalo = lance.cavalo if lance else "Cavalo Desconhecido"
    valor_lance = lance.valor if lance else "R$ 0,00"
    nome_cliente = lance.usuario.perfil_cliente.nome_completo if lance and hasattr(lance.usuario, 'perfil_cliente') else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = cliente.username.email if cliente else settings.DEFAULT_FROM_EMAIL

    context = {
        'url_site': 'https://www.virtualstables.com.br/',
        'title_email': "Lance Coberto",
        'primeiro_nome': primeiro_nome,
        'valor_lance': valor_lance,
        'cavalo': cavalo,
    }
    html_content = render_to_string('partials/lance_coberto.html', context)
    text_content = strip_tags(html_content)
    subject = f"Lance Coberto - {nome_cliente}" if cliente else "Lance Coberto"
    email = EmailMultiAlternatives(
        #subject
        subject,
        #content
        text_content,
        #from email
        settings.DEFAULT_FROM_EMAIL,
        #to
        [email_cliente],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()