from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)


def send_email(html_content, text_content, subject, recipient_list):
    """
    Função auxiliar para enviar e-mails
    """
    try:
        # Tenta primeiro com EmailMultiAlternatives do Django (funciona melhor em produção)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        
        logger.info(f'✅ E-mail enviado (Django) para: {", ".join(recipient_list)}')
        
    except Exception as django_error:
        logger.warning(f'⚠️ Falha com método Django: {str(django_error)}')
        logger.info('🔄 Tentando método alternativo com smtplib...')
        
        # Fallback: tenta com smtplib diretamente
        try:
            for recipient in recipient_list:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = settings.DEFAULT_FROM_EMAIL
                msg['To'] = recipient
                
                part1 = MIMEText(text_content, 'plain')
                part2 = MIMEText(html_content, 'html')
                msg.attach(part1)
                msg.attach(part2)
                
                context_ssl = ssl.create_default_context()
                if settings.DEBUG:
                    context_ssl.check_hostname = False
                    context_ssl.verify_mode = ssl.CERT_NONE
                
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=30) as server:
                    server.starttls(context=context_ssl)
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.send_message(msg)
                
                logger.info(f'✅ E-mail enviado (smtplib) para: {recipient}')
                
        except Exception as smtp_error:
            error_msg = f'❌ Erro final ao enviar e-mail: {str(smtp_error)}'
            logger.error(error_msg)
            raise Exception(error_msg)