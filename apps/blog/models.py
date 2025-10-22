from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

class Post(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(max_length=220, unique=True, blank=True, help_text='Deixe em branco para gerar automaticamente a partir do título.')
    autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Autor')
    # categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='Categoria')
    resumo = models.CharField(max_length=300, blank=True, verbose_name='Resumo')   
    conteudo = models.TextField(verbose_name='Conteúdo')
    imagem = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name='Imagem de Destaque')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    published = models.BooleanField(default=True, verbose_name='Publicado')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('blog_frontend:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Opinião"
        verbose_name_plural = "Opiniões"