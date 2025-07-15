from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.leilao.models import Leilao, Lance, Cavalo

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    # Criar permissões customizadas
    content_type_leilao = ContentType.objects.get_for_model(Leilao)
    content_type_lance = ContentType.objects.get_for_model(Lance)
    content_type_cavalo = ContentType.objects.get_for_model(Cavalo)

    Permission.objects.get_or_create(
        codename='can_bid',
        name='Pode dar lances no leilão',
        content_type=content_type_lance,
    )
    Permission.objects.get_or_create(
        codename='can_end_auction',
        name='Pode encerrar leilões',
        content_type=content_type_leilao,
    )

    # Criar grupos
    clientes, _ = Group.objects.get_or_create(name='Clientes')
    vendedores, _ = Group.objects.get_or_create(name='Vendedores')
    gerentes, _ = Group.objects.get_or_create(name='Gerentes')
    administradores, _ = Group.objects.get_or_create(name='Administradores')

    # Atribuir permissões
    clientes.permissions.set([
        Permission.objects.get(codename='view_leilao'),
        Permission.objects.get(codename='view_cavalo'),
        Permission.objects.get(codename='can_bid'),
    ])
    vendedores.permissions.set([
        Permission.objects.get(codename='view_leilao'),
        Permission.objects.get(codename='add_cavalo'),
        Permission.objects.get(codename='change_cavalo'),
        Permission.objects.get(codename='view_cavalo'),
    ])
    gerentes.permissions.set([
        Permission.objects.get(codename='add_leilao'),
        Permission.objects.get(codename='change_leilao'),
        Permission.objects.get(codename='view_leilao'),
        Permission.objects.get(codename='add_cavalo'),
        Permission.objects.get(codename='change_cavalo'),
        Permission.objects.get(codename='view_cavalo'),
    ])
    administradores.permissions.set(Permission.objects.all())