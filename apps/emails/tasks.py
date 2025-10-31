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
        'name_site': settings.PAINEL_TITLE,
        'url_site': settings.URL_SITE,
        'title_email': title_email,
        'primeiro_nome': primeiro_nome
    }
    html_content = render_to_string('partials/cadastro_confirmado.html', context)
    text_content = strip_tags(html_content)
    subject = f"{title_email}"
    # Enviar E-mail
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
    # Enviar E-mail
    send_email(html_content, text_content, subject, [email_cliente])

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
    # Enviar E-mail
    send_email(html_content, text_content, subject, [email_cliente])

@shared_task
def email_recuperacao_senha(user_id, uid, token):
    """Envia e-mail de recuperação de senha"""
    try:
        user = User.objects.get(id=user_id)
        
        # Usa apenas as configurações do settings.py
        site_name = getattr(settings, 'PAINEL_TITLE', 'Virtual Stables')
        site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
        
        # URL de reset
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
        
        # Criar conexão SMTP customizada para desenvolvimento (ignora SSL)
        if settings.DEBUG:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            
            try:
                # Criar mensagem MIME
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f'{site_name} - Recuperação de Senha'
                msg['From'] = settings.DEFAULT_FROM_EMAIL
                msg['To'] = user.email
                
                # Adicionar HTML
                part1 = MIMEText(plain_message, 'plain')
                part2 = MIMEText(html_message, 'html')
                msg.attach(part1)
                msg.attach(part2)
                
                # Conectar ao servidor SMTP sem verificação SSL
                context_ssl = ssl.create_default_context()
                context_ssl.check_hostname = False
                context_ssl.verify_mode = ssl.CERT_NONE
                
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                    server.starttls(context=context_ssl)
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.send_message(msg)
                
                logger.info(f'✅ E-mail de recuperação enviado para {user.email}')
                logger.warning('=' * 80)
                logger.warning('RECUPERAÇÃO DE SENHA - E-MAIL ENVIADO')
                logger.warning(f'Destinatário: {user.email}')
                logger.warning(f'Link de recuperação: {reset_url}')
                logger.warning('=' * 80)
                return f'E-mail de recuperação enviado para {user.email}'
                
            except Exception as smtp_error:
                logger.error(f'❌ Erro ao enviar e-mail: {str(smtp_error)}')
                logger.warning('=' * 80)
                logger.warning('RECUPERAÇÃO DE SENHA - ERRO NO ENVIO')
                logger.warning(f'Link de recuperação (use este link): {reset_url}')
                logger.warning('=' * 80)
                return f'Erro ao enviar, mas link gerado: {reset_url}'
        
        # Em produção, usa o método padrão do Django
        else:
            email = EmailMessage(
                subject=f'{site_name} - Recuperação de Senha',
                body=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            
            logger.info(f'E-mail de recuperação enviado para {user.email}')
            return f'E-mail de recuperação enviado para {user.email}'
        
    except User.DoesNotExist:
        error_msg = f'Usuário com ID {user_id} não encontrado'
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f'Erro ao enviar e-mail: {str(e)}'
        logger.error(error_msg)
        return error_msg