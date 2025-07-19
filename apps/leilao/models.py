from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from apps.cavalo.models import Cavalo


class Leilao(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome do leilão")
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True, help_text="Descrição detalhada do leilão")
    termos = models.TextField(blank=True, null=True, help_text="Termos do leilão")
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.leilao.atualizar_lance_atual()

    def __str__(self):
        return f"Lance de R${self.valor} por {self.usuario.username} em {self.leilao}"

    def clean(self):
        if self.leilao.status != 'ativo':
            raise ValidationError("Não é possível dar lances em leilões finalizados.")
        if self.valor <= self.leilao.lance_inicial:
            raise ValidationError("O lance deve ser maior que o lance inicial.")
        ultimo_lance = self.leilao.lances.order_by('-valor').first()
        if ultimo_lance and self.valor <= ultimo_lance.valor:
            raise ValidationError("O lance deve ser maior que o último lance.")