from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilCliente(models.Model):
    
    ESTADOS_BRASIL = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]    
    
    STATUS_CHOICES = [
        ('analise', 'Em Análise'),
        ('ativo', 'Aprovado'),
        ('inativo', 'Recusado'),
        ('suspenso', 'Suspenso'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    
    nome_completo = models.CharField(
        max_length=100, 
        verbose_name="Nome Completo",
        help_text="Nome completo do cliente"
    )
    
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF deve estar no formato 000.000.000-00')],
        verbose_name="CPF",
        help_text="Pessoa Física - Formato: 000.000.000-00"
    )
    
    # ... resto dos campos permanece igual
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', 'CNPJ deve estar no formato 00.000.000/0000-00')],
        verbose_name="CNPJ",
        help_text="Pessoa Jurídica - Formato: 00.000.000/0000-00"
    )

    rg_ie = models.CharField(max_length=15, verbose_name="RG/IE")
    emis_uf = models.CharField(
        max_length=2,
        choices=ESTADOS_BRASIL,
        verbose_name="UF de Emissão",
        help_text="Selecione o estado"
    )
    nasc_fund = models.DateField(verbose_name="Data de Nascimento/Fundação", help_text="Formato: DD/MM/AAAA")
    profis_cnae = models.CharField(max_length=25, blank=True, null=True, verbose_name="Profissão/CNAE", help_text="Código CNAE ou profissão")
    end_rua_av = models.CharField(max_length=200, verbose_name="Rua/Avenida")
    end_numero = models.CharField(max_length=10, verbose_name="Número")
    end_complem = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    end_bairro = models.CharField(max_length=100, verbose_name="Bairro")
    end_cidade = models.CharField(max_length=100, verbose_name="Cidade")
    end_estado = models.CharField(
        max_length=2,
        choices=ESTADOS_BRASIL,
        verbose_name="Estado",
        help_text="Selecione o estado"
    )
    end_cep = models.CharField(
        max_length=9,
        validators=[RegexValidator(r'^\d{5}-\d{3}$', 'CEP deve estar no formato 00000-000')],
        verbose_name="CEP",
        help_text="Formato: 00000-000"
    )
    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\(\d{2}\) \d{4}-\d{4}$', 'Telefone deve estar no formato (11) 1234-5678')],
        verbose_name="Telefone",
        help_text="Formato: (11) 1234-5678"
    )
    celular = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(\d{2}\) 9\d{4}-\d{4}$', 'Celular deve estar no formato (11) 91234-5678')],
        verbose_name="Celular",
        help_text="Formato: (11) 91234-5678"
    )
    propriedade = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nome da Propriedade", help_text="Nome do Propriedade, se aplicável")
    propr_cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade da Propriedade")
    propr_estado = models.CharField(
        max_length=2,
        blank=True, null=True,
        choices=ESTADOS_BRASIL,
        verbose_name="Estado da Propriedade",
        help_text="Selecione o estado"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='analise',
        verbose_name="Status",
        help_text="Status atual do cliente no sistema"
    )

    def __str__(self):
        return f"Perfil de {self.usuario.username} - {self.nome_completo} ({self.get_status_display()})"
    
    def pode_dar_lances(self):
        """Verifica se o cliente pode dar lances (status ativo)"""
        return self.status == 'ativo'
    
    class Meta:
        verbose_name = "Perfil do Cliente"
        verbose_name_plural = "Perfis dos Clientes"

@receiver(post_save, sender=PerfilCliente)
def atribuir_permissao_cliente(sender, instance, created, **kwargs):
    """
    Signal para atribuir automaticamente a permissão 'Clientes' 
    quando um perfil de cliente é criado
    """
    if created:
        try:
            grupo_cliente = Group.objects.get(name='Clientes')
            instance.usuario.groups.add(grupo_cliente)
        except Group.DoesNotExist:
            # Log ou criar o grupo se não existir
            grupo_cliente = Group.objects.create(name='Clientes')
            instance.usuario.groups.add(grupo_cliente)