from django.db import models

class SiteSettings(models.Model):
    email = models.EmailField(max_length=255)
    telefone = models.CharField(max_length=20)
    facebook = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    youtube = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return "Configurações do Site"

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"

class Banner(models.Model):
    titulo = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='banners/')
    link = models.URLField(max_length=255, blank=True)
    ordem = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

class Logo(models.Model):
    titulo = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='logos/')
    link = models.URLField(max_length=255, blank=True)
    ordem = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.imagem.name

    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Logos"