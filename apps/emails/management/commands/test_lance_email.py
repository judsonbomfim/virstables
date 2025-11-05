from django.core.management.base import BaseCommand
from apps.emails.tasks import email_lance_confirmado
from apps.leilao.models import Lance


class Command(BaseCommand):
    help = 'Testa o envio de e-mail de lance confirmado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--lance_id',
            type=int,
            help='ID do lance para teste',
            required=True
        )

    def handle(self, *args, **options):
        lance_id = options['lance_id']
        
        try:
            lance = Lance.objects.get(pk=lance_id)
            self.stdout.write(self.style.WARNING('=' * 80))
            self.stdout.write(self.style.WARNING('TESTE DE E-MAIL DE LANCE'))
            self.stdout.write(self.style.WARNING('=' * 80))
            self.stdout.write(f'\n📋 Lance ID: {lance_id}')
            self.stdout.write(f'🐴 Cavalo: {lance.cavalo}')
            self.stdout.write(f'💰 Valor: R$ {lance.valor}')
            self.stdout.write(f'👤 Usuário: {lance.usuario.email}')
            self.stdout.write(f'\n🚀 Enviando e-mail...\n')
            
            # Executar task
            result = email_lance_confirmado.delay(lance_id)
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ Task executada: {result.id}'))
            self.stdout.write(self.style.WARNING('Verifique os logs do Celery para mais detalhes'))
            self.stdout.write('=' * 80 + '\n')
            
        except Lance.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Lance #{lance_id} não encontrado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro: {str(e)}'))