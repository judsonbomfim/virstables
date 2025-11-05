from django.contrib import admin
from .models import Cavalo, Foto, Video

class FotoInline(admin.TabularInline):
    model = Foto
    extra = 1
    fields = ['imagem', 'is_destaque', 'ordem']
    ordering = ['ordem']

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ['url_youtube', 'legenda']

@admin.register(Cavalo)
class CavaloAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 
        'raca', 
        'sexo', 
        'leilao', 
        'lance_inicial', 
        'incremento_lance',
        'status', 
        'data_cadastro'
    ]
    
    list_filter = [
        'status', 
        'sexo', 
        'raca', 
        'leilao', 
        'data_cadastro'
    ]
    
    search_fields = [
        'nome', 
        'registro', 
        'raca', 
        'criador', 
        'vendedor',
        'pai',
        'mae'
    ]
    
    list_editable = ['status', 'lance_inicial', 'incremento_lance']
    
    prepopulated_fields = {'slug': ('nome',)}
    readonly_fields = ['slug', 'data_cadastro']
    
    autocomplete_fields = ['leilao']
    
    inlines = [FotoInline, VideoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'nome', 
                'slug', 
                'raca', 
                'registro', 
                'descricao',
                'leilao'
            )
        }),
        ('Características Físicas', {
            'fields': (
                'sexo', 
                'nascimento', 
                'altura', 
                'pelagem',
                'geracao'
            )
        }),
        ('Genealogia - Pais', {
            'fields': ('pai', 'mae'),
            'classes': ('collapse',)
        }),
        ('Genealogia - Avós', {
            'fields': (
                'avo_paterno', 
                'avo_paterna', 
                'avo_materno', 
                'avo_materna'
            ),
            'classes': ('collapse',)
        }),
        ('Genealogia - Bisavós Paternos', {
            'fields': (
                'bisavo_paterno1', 
                'bisavo_paterno2', 
                'bisavo_paterno3', 
                'bisavo_paterno4'
            ),
            'classes': ('collapse',)
        }),
        ('Genealogia - Bisavós Maternos', {
            'fields': (
                'bisavo_materno1', 
                'bisavo_materno2', 
                'bisavo_materno3', 
                'bisavo_materno4'
            ),
            'classes': ('collapse',)
        }),
        ('Informações Comerciais', {
            'fields': (
                'criador', 
                'vendedor', 
                'alojamento'
            )
        }),
        ('Leilão e Valores', {
            'fields': (
                'lance_inicial', 
                'incremento_lance', 
                'parcela', 
                'status'
            )
        }),
        ('Sistema', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'data_cadastro'

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ['cavalo', 'is_destaque', 'ordem', 'imagem']
    list_filter = ['is_destaque', 'cavalo__leilao']
    search_fields = ['cavalo__nome']
    list_editable = ['is_destaque', 'ordem']
    autocomplete_fields = ['cavalo']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cavalo')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['cavalo', 'legenda', 'url_youtube']
    list_filter = ['cavalo__leilao']
    search_fields = ['cavalo__nome', 'legenda']
    autocomplete_fields = ['cavalo']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cavalo')

# Ações personalizadas
@admin.action(description='Marcar como disponível')
def marcar_disponivel(modeladmin, request, queryset):
    queryset.update(status='disponivel')

@admin.action(description='Marcar como vendido')
def marcar_vendido(modeladmin, request, queryset):
    queryset.update(status='vendido')

@admin.action(description='Marcar como reservado')
def marcar_reservado(modeladmin, request, queryset):
    queryset.update(status='reservado')

# Adicionar ações ao CavaloAdmin
CavaloAdmin.actions = [marcar_disponivel, marcar_vendido, marcar_reservado]