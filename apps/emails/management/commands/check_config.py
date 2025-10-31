from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Verifica as configurações do sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=' * 80))
        self.stdout.write(self.style.WARNING('CONFIGURAÇÕES DO SISTEMA'))
        self.stdout.write(self.style.WARNING('=' * 80))
        
        configs = [
            ('DEBUG', settings.DEBUG),
            ('PAINEL_TITLE', settings.PAINEL_TITLE),
            ('URL_SITE', settings.URL_SITE),
            ('SITE_URL', getattr(settings, 'SITE_URL', 'NÃO DEFINIDO')),
            ('DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL),
            ('EMAIL_HOST', settings.EMAIL_HOST),
            ('EMAIL_PORT', settings.EMAIL_PORT),
            ('EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
        ]
        
        for key, value in configs:
            color = self.style.SUCCESS if value else self.style.ERROR
            self.stdout.write(f'{key}: {color(str(value))}')
        
        self.stdout.write('\n' + '=' * 80)