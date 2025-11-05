from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.leilao.models import Leilao, Lance, Cavalo

@receiver(post_migrate, sender=Leilao._meta.app_config)
def create_groups_and_permissions(sender, **kwargs):
    # Criar permissões customizadas
    content_type_leilao = ContentType.objects.get_for_model(Leilao)
    content_type_lance = ContentType.objects.get_for_model(Lance)
    content_type_cavalo = ContentType.objects.get_for_model(Cavalo)

    # Criar ou obter permissões
    view_leilao, _ = Permission.objects.get_or_create(
        codename='view_leilao',
        name='Can view leilao',
        content_type=content_type_leilao,
    )
    view_cavalo, _ = Permission.objects.get_or_create(
        codename='view_cavalo',
        name='Can view cavalo',
        content_type=content_type_cavalo,
    )
    add_cavalo, _ = Permission.objects.get_or_create(
        codename='add_cavalo',
        name='Can add cavalo',
        content_type=content_type_cavalo,
    )
    change_cavalo, _ = Permission.objects.get_or_create(
        codename='change_cavalo',
        name='Can change cavalo',
        content_type=content_type_cavalo,
    )
    add_leilao, _ = Permission.objects.get_or_create(
        codename='add_leilao',
        name='Can add leilao',
        content_type=content_type_leilao,
    )
    change_leilao, _ = Permission.objects.get_or_create(
        codename='change_leilao',
        name='Can change leilao',
        content_type=content_type_leilao,
    )
    can_bid, _ = Permission.objects.get_or_create(
        codename='can_bid',
        name='Pode dar lances no leilão',
        content_type=content_type_lance,
    )
    can_end_auction, _ = Permission.objects.get_or_create(
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
        view_leilao,
        view_cavalo,
        can_bid,
    ])
    vendedores.permissions.set([
        view_leilao,
        add_cavalo,
        change_cavalo,
        view_cavalo,
    ])
    gerentes.permissions.set([
        add_leilao,
        change_leilao,
        view_leilao,
        add_cavalo,
        change_cavalo,
        view_cavalo,
    ])
    administradores.permissions.set(Permission.objects.all())