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
        # Em desenvolvimento, usa o método que funciona (mesmo do test_email)
        if settings.DEBUG:
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
                context_ssl.check_hostname = False
                context_ssl.verify_mode = ssl.CERT_NONE
                
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                    server.starttls(context=context_ssl)
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.send_message(msg)
                
                logger.info(f'✅ E-mail enviado para: {recipient}')
        else:
            # Em produção, usa o método padrão do Django
            send_mail(
                subject=subject,
                message=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_content,
                fail_silently=False,
            )
            logger.info(f'✅ E-mails enviados para: {", ".join(recipient_list)}')
            
    except Exception as e:
        logger.error(f'❌ Erro ao enviar e-mail: {str(e)}')
        raise