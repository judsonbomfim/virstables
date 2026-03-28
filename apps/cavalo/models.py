from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


from django.utils.text import slugify
class Cavalo(models.Model):
    leilao = models.ForeignKey(
        'leilao.Leilao',  # referência em string: 'app.Model'
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cavalos_leilao',
        help_text="Leilão ao qual o cavalo está vinculado (opcional)"
    )
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    raca = models.CharField(max_length=50, null=True)
    descricao = models.TextField()
    registro = models.CharField(
        max_length=50,
    )
    nascimento = models.DateField(blank=True, null=True, help_text="Data de nascimento do cavalo")
    geracao = models.CharField(max_length=50, blank=True, null=True, help_text="Geração do cavalo")
    altura = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, help_text="Altura em metros")
    sexo = models.CharField(max_length=10, blank=True, null=True, choices=[('M', 'Macho'), ('F', 'Fêmea'), ('C', 'Castrado')])
    pelagem = models.CharField(max_length=30, blank=True, null=True, help_text="Tipo de pelagem")
    criador = models.CharField(max_length=100, blank=True, null=True, help_text="Criador do cavalo")
    vendedor = models.CharField(max_length=100, blank=True, null=True, help_text="Vendedor do cavalo")
    alojamento = models.CharField(max_length=100, blank=True, null=True, help_text="Local de alojamento do cavalo")
    # Genealogia
    pai = models.CharField(max_length=30, blank=True, null=True, help_text="Pai do cavalo")
    mae = models.CharField(max_length=30, blank=True, null=True, help_text="Mãe do cavalo")
    avo_paterno = models.CharField(max_length=30, blank=True, null=True, help_text="Avô Paterno")
    avo_paterna = models.CharField(max_length=30, blank=True, null=True, help_text="Avó Paterna")
    avo_materno = models.CharField(max_length=30, blank=True, null=True, help_text="Avô Materno")
    avo_materna = models.CharField(max_length=30, blank=True, null=True, help_text="Avó Materna")
    bisavo_paterno1 = models.CharField(max_length=30, blank=True, null=True, help_text="Bisavô Paterno")
    bisavo_paterno2 = models.CharField(max_length=30, blank=True, null=True, help_text="Bisavó Paterno")
    bisavo_paterno3 = models.CharField(max_length=30, blank=True, null=True, help_text="Bisavô Paterno")
    bisavo_paterno4 = models.CharField(max_length=30, blank=True, null=True, help_text="Bisavó Paterno")
    bisavo_materno1 = models.CharField(max_length=30, blank=True, null=True, help_text="Bisavô Materno")
    bisavo_materno2 = models.CharField(max_length=30, blank=True, null=True, help_text="Bisavó Materno")
    bisavo_materno3 = models.CharField(max_length=30, blank=True, null=True, help_text="Bisavô Materno")
    bisavo_materno4 = models.CharField(max_length=30, blank=True, null=True, help_text="Bisavó Materno")
    lance_inicial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Lance Inicial da parcela")
    incremento_lance = models.DecimalField(max_digits=10, decimal_places=2, default=50.00, help_text="Valor mínimo de incremento entre lances")
    parcela = models.IntegerField(blank=True, null=True, help_text="Número de parcelas")
    lote = models.IntegerField(blank=True, null=True, help_text="Número do lote no leilão")
    data_cadastro = models.DateTimeField(auto_now_add=True, help_text="Data de cadastro do cavalo")
    status = models.CharField(
        max_length=20,
        choices=[('disponivel', 'Disponível'), ('vendido', 'Vendido'), ('reservado', 'Reservado')],
        default='disponivel',
        help_text="Status do cavalo"
    )
    
    class Meta:
        unique_together = ['leilao', 'lote']
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        novo_slug = slugify(self.nome)
        slug_unico = novo_slug
        contador = 1
        while Cavalo.objects.filter(slug=slug_unico).exclude(pk=self.pk).exists():
            slug_unico = f"{novo_slug}-{contador}"
            contador += 1
        self.slug = slug_unico
        super().save(*args, **kwargs)

class Foto(models.Model):
    cavalo = models.ForeignKey('Cavalo', on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='fotos_cavalos/', blank=True, null=True, default='leiloes/default.jpg')
    is_destaque = models.BooleanField(default=False)
    ordem = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.is_destaque:
            # Desmarca o destaque das outras fotos deste cavalo
            Foto.objects.filter(cavalo=self.cavalo, is_destaque=True).exclude(pk=self.pk).update(is_destaque=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Foto de {self.cavalo.nome}"

class Video(models.Model):
    cavalo = models.ForeignKey(Cavalo, on_delete=models.CASCADE, related_name='videos')
    url_youtube = models.URLField()
    legenda = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Vídeo de {self.cavalo.nome}"