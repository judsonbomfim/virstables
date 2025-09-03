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