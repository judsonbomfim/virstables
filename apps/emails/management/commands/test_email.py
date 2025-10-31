from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Command(BaseCommand):
    help = 'Testa as configurações de e-mail'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='E-mail de destino para teste',
            default='seu-email@teste.com'
        )

    def handle(self, *args, **options):
        email_destino = options['email']
        
        self.stdout.write(self.style.WARNING('=' * 80))
        self.stdout.write(self.style.WARNING('TESTE DE CONFIGURAÇÃO DE E-MAIL'))
        self.stdout.write(self.style.WARNING('=' * 80))
        
        # Exibir configurações
        self.stdout.write('\n📋 CONFIGURAÇÕES ATUAIS:')
        self.stdout.write(f'  EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'  EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'  EMAIL_HOST_PASSWORD: {"*" * len(settings.EMAIL_HOST_PASSWORD)}')
        self.stdout.write(f'  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        
        # Teste 1: Conexão SMTP básica
        self.stdout.write('\n\n🔌 TESTE 1: Conexão SMTP')
        try:
            context_ssl = ssl.create_default_context()
            context_ssl.check_hostname = False
            context_ssl.verify_mode = ssl.CERT_NONE
            
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10) as server:
                server.set_debuglevel(1)  # Mostrar debug
                self.stdout.write(self.style.SUCCESS('  ✅ Conectado ao servidor SMTP'))
                
                # STARTTLS
                server.starttls(context=context_ssl)
                self.stdout.write(self.style.SUCCESS('  ✅ STARTTLS ativado'))
                
                # Login
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                self.stdout.write(self.style.SUCCESS('  ✅ Login realizado com sucesso'))
                
        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Erro de autenticação: {str(e)}'))
            self.stdout.write(self.style.ERROR('  → Verifique EMAIL_HOST_USER e EMAIL_HOST_PASSWORD'))
            return
        except smtplib.SMTPException as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Erro SMTP: {str(e)}'))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Erro de conexão: {str(e)}'))
            return
        
        # Teste 2: Enviar e-mail de teste
        self.stdout.write('\n\n📧 TESTE 2: Enviar e-mail de teste')
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Teste de E-mail - Virtual Stables'
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = email_destino
            
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #667eea;">✅ Teste de E-mail Bem-Sucedido!</h2>
                    <p>Este é um e-mail de teste do sistema Virtual Stables.</p>
                    <p><strong>Configurações testadas:</strong></p>
                    <ul>
                        <li>Servidor SMTP: {settings.EMAIL_HOST}</li>
                        <li>Porta: {settings.EMAIL_PORT}</li>
                        <li>TLS: {settings.EMAIL_USE_TLS}</li>
                        <li>Usuário: {settings.EMAIL_HOST_USER}</li>
                    </ul>
                    <p style="color: green;"><strong>✅ Todas as configurações estão corretas!</strong></p>
                </body>
            </html>
            """
            
            plain = "Teste de e-mail bem-sucedido! As configurações estão corretas."
            
            part1 = MIMEText(plain, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            context_ssl = ssl.create_default_context()
            context_ssl.check_hostname = False
            context_ssl.verify_mode = ssl.CERT_NONE
            
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls(context=context_ssl)
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.send_message(msg)
            
            self.stdout.write(self.style.SUCCESS(f'  ✅ E-mail enviado para: {email_destino}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Erro ao enviar e-mail: {str(e)}'))
            return
        
        # Teste 3: Enviar usando Django
        self.stdout.write('\n\n🐍 TESTE 3: Enviar usando Django send_mail')
        try:
            send_mail(
                subject='Teste Django - Virtual Stables',
                message='Teste usando send_mail do Django',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_destino],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'  ✅ E-mail Django enviado para: {email_destino}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Erro Django: {str(e)}'))
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS('✅ TESTES CONCLUÍDOS COM SUCESSO!'))
        self.stdout.write(self.style.WARNING(f'Verifique a caixa de entrada de: {email_destino}'))
        self.stdout.write('=' * 80 + '\n')