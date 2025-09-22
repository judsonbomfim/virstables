from django.contrib import admin
from .models import Leilao, Lance

@admin.register(Leilao)
class LeilaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'status', 'data_inicio', 'data_fim', 'data_leilao']
    list_filter = ['status', 'data_inicio', 'data_fim']
    search_fields = ['nome', 'descricao']
    list_editable = ['status']
    prepopulated_fields = {'slug': ('nome',)}
    readonly_fields = ['slug']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'slug', 'descricao', 'imagem')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_fim', 'data_leilao')
        }),
        ('Configurações', {
            'fields': ('status', 'termos')
        }),
    )
    
    date_hierarchy = 'data_inicio'

@admin.register(Lance)
class LanceAdmin(admin.ModelAdmin):
    list_display = ['leilao', 'cavalo', 'usuario', 'valor', 'data']
    list_filter = ['leilao', 'data', 'leilao__status']
    search_fields = ['usuario__username', 'cavalo__nome', 'leilao__nome']
    readonly_fields = ['data']
    autocomplete_fields = ['leilao', 'cavalo', 'usuario']
    
    fieldsets = (
        ('Lance', {
            'fields': ('leilao', 'cavalo', 'usuario', 'valor')
        }),
        ('Informações do Sistema', {
            'fields': ('data',),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'data'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando um lance existente
            return self.readonly_fields + ['leilao', 'cavalo', 'usuario']
        return self.readonly_fields

# Ações personalizadas
@admin.action(description='Finalizar leilões selecionados')
def finalizar_leiloes(modeladmin, request, queryset):
    queryset.update(status='finalizado')

# Adicionar ação ao LeilaoAdmin
LeilaoAdmin.actions = [finalizar_leiloes]