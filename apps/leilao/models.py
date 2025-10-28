from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from apps.cavalo.models import Cavalo


class Leilao(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome do leilão")
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True, help_text="Descrição detalhada do leilão")
    termos = models.FileField(
        upload_to='leilao/termos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Arquivo PDF com os termos do leilão",
        verbose_name="Termos do Leilão (PDF)"
    )
    data_leilao = models.DateTimeField(null=True, blank=True, help_text="Data e hora do leilão")
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    imagem = models.ImageField(upload_to='leilao/')
    status = models.CharField(max_length=20, choices=[('ativo', 'Ativo'), ('finalizado', 'Finalizado')], default='ativo')

    def __str__(self):
        return str(self.nome)

    def save(self, *args, **kwargs):
        novo_slug = slugify(self.nome)
        slug_unico = novo_slug
        contador = 1
        while Leilao.objects.filter(slug=slug_unico).exclude(pk=self.pk).exists():  # type: ignore
            slug_unico = f"{novo_slug}-{contador}"
            contador += 1
        self.slug = slug_unico
        super().save(*args, **kwargs)

class Lance(models.Model):
    leilao = models.ForeignKey(Leilao, on_delete=models.CASCADE, related_name='lance_leilao')
    cavalo = models.ForeignKey(Cavalo, on_delete=models.CASCADE, related_name='lance_cavalo')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lance de R${self.valor} por {self.usuario.username} em {self.leilao}"

def clean(self):
    from django.core.exceptions import ValidationError
    
    # Validar se os campos obrigatórios existem
    if not hasattr(self.cavalo, 'incremento_lance') or self.cavalo.incremento_lance is None:
        raise ValidationError('O cavalo não possui incremento de lance configurado.')
    
    if not hasattr(self.cavalo, 'lance_inicial') or self.cavalo.lance_inicial is None:
        raise ValidationError('O cavalo não possui lance inicial configurado.')
    
    # Verificar se há lance anterior
    ultimo_lance = Lance.objects.filter(cavalo=self.cavalo).order_by('-valor').first()
    
    if ultimo_lance:
        # Lance deve ser maior que o anterior + incremento
        valor_minimo = ultimo_lance.valor + self.cavalo.incremento_lance
        if self.valor < valor_minimo:
            raise ValidationError(f'O lance deve ser de pelo menos R$ {valor_minimo:.2f}')
        
        # NOVA VALIDAÇÃO: Verificar se é múltiplo do incremento
        diferenca = self.valor - ultimo_lance.valor
        if diferenca % self.cavalo.incremento_lance != 0:
            raise ValidationError(f'O lance deve ser um múltiplo de R$ {self.cavalo.incremento_lance:.2f} acima do lance anterior.')
            
    else:
        # Primeiro lance deve ser maior ou igual ao lance inicial
        if self.valor < self.cavalo.lance_inicial:
            raise ValidationError(f'O lance deve ser de pelo menos R$ {self.cavalo.lance_inicial:.2f}')
        
        # NOVA VALIDAÇÃO: Verificar se é múltiplo do incremento a partir do lance inicial
        diferenca = self.valor - self.cavalo.lance_inicial
        if diferenca % self.cavalo.incremento_lance != 0:
            raise ValidationError(f'O lance deve ser o lance inicial (R$ {self.cavalo.lance_inicial:.2f}) ou um múltiplo de R$ {self.cavalo.incremento_lance:.2f} acima dele.')
    
    # Verificar se o leilão está ativo
    if self.leilao.status != 'ativo':
        raise ValidationError('Não é possível dar lance em leilão inativo.')