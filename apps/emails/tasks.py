from urllib import request
from celery import shared_task
from django.core.mail import send_mail, EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from apps.emails.classes import send_email
from apps.leilao.models import Lance
from apps.users.models import PerfilCliente
import logging
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

@shared_task
def email_cadastro_analise(id):
    cliente = PerfilCliente.objects.get(pk=id) if id else None
    nome_cliente = cliente.nome_completo if cliente else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = cliente.usuario.email if cliente else settings.DEFAULT_FROM_EMAIL
    title_email = "Confirmação em Análise"

    context = {
        'name_site': settings.PAINEL_TITLE,
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome
    }
    html_content = render_to_string('partials/cadastro_analise.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email}"
    send_email(html_content, text_content, subject, [email_cliente])

@shared_task
def email_cadastro_confirmado(id):
    cliente = PerfilCliente.objects.get(pk=id) if id else None
    nome_cliente = cliente.nome_completo if cliente else "Cliente"
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = cliente.usuario.email if cliente else settings.DEFAULT_FROM_EMAIL
    title_email = "Confirmação de Cadastro"
    
    context = {
        'name_site': settings.PAINEL_TITLE,
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome
    }
    html_content = render_to_string('partials/cadastro_confirmado.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email}"
    send_email(html_content, text_content, subject, [email_cliente])

@shared_task
def email_lance_confirmado(id):
    print(">>>>> Enviando email de lance confirmado")
    lance = Lance.objects.get(pk=id)    
    cavalo = str(lance.cavalo)
    valor_lance = f"R$ {lance.valor}"
    nome_cliente = str(lance.usuario.perfil_cliente.nome_completo)
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = lance.usuario.email
    title_email = f'Lance Confirmado - {cavalo}'
    
    context = {
        'name_site': settings.PAINEL_TITLE,
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome,
        'valor_lance': valor_lance,
        'cavalo': cavalo,
    }
    html_content = render_to_string('partials/lance_confirmado.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email}"
    
    logger.info(f'📧 Enviando e-mail de lance confirmado para: {email_cliente}')
    send_email(html_content, text_content, subject, [email_cliente])
    logger.info(f'✅ E-mail de lance confirmado enviado com sucesso')

@shared_task
def email_lance_coberto(id):
    lance = Lance.objects.get(pk=id)    
    cavalo = str(lance.cavalo)
    valor_lance = f"R$ {lance.valor}"
    nome_cliente = str(lance.usuario.perfil_cliente.nome_completo)
    primeiro_nome = nome_cliente.split()[0] if nome_cliente else "Cliente"
    email_cliente = lance.usuario.email
    title_email = f"Lance Coberto - {cavalo}"

    context = {
        'name_site': settings.PAINEL_TITLE,
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome,
        'valor_lance': valor_lance,
        'cavalo': cavalo,
    }
    html_content = render_to_string('partials/lance_coberto.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email}"
    
    logger.info(f'📧 Enviando e-mail de lance coberto para: {email_cliente}')
    send_email(html_content, text_content, subject, [email_cliente])
    logger.info(f'✅ E-mail de lance coberto enviado com sucesso')

@shared_task
def email_recuperacao_senha(user_id, uid, token):
    """Envia e-mail de recuperação de senha"""
    try:
        user = User.objects.get(id=user_id)
        
        # Usa URL_SITE do settings (remove barra final se existir)
        site_name = getattr(settings, 'PAINEL_TITLE', 'Virtual Stables')
        site_url = getattr(settings, 'URL_SITE', 'http://localhost:8000').rstrip('/')
        
        # URL de reset (sem barra dupla)
        reset_url = f"{site_url}/reset/{uid}/{token}/"
        
        # Contexto do e-mail
        context = {
            'user': user,
            'reset_url': reset_url,
            'site_name': site_name,
            'site_url': site_url,
        }
        
        # Renderizar template HTML
        html_message = render_to_string('emails/recuperacao_senha.html', context)
        plain_message = strip_tags(html_message)
        
        subject = f'{site_name} - Recuperação de Senha'
        
        logger.info(f'📧 Enviando e-mail de recuperação para: {user.email}')
        logger.info(f'🔗 Link de recuperação: {reset_url}')
        logger.info(f'🌐 URL base usada: {site_url}')
        
        # Usar a função send_email
        send_email(html_message, plain_message, subject, [user.email])
        
        logger.info(f'✅ E-mail de recuperação enviado com sucesso para {user.email}')
        return f'E-mail de recuperação enviado para {user.email}'
        
    except User.DoesNotExist:
        error_msg = f'Usuário com ID {user_id} não encontrado'
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f'❌ Erro ao enviar e-mail: {str(e)}'
        logger.error(error_msg)
        raise