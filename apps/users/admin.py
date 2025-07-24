from django.contrib import admin
from .models import PerfilCliente

@admin.register(PerfilCliente)
class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome_completo', 
        'usuario', 
        'cpf', 
        'celular', 
        'end_cidade', 
        'end_estado', 
        'status'
    ]
    
    list_filter = [
        'status', 
        'end_estado', 
        'emis_uf', 
        'propr_estado'
    ]
    
    search_fields = [
        'nome_completo', 
        'cpf', 
        'cnpj', 
        'usuario__username', 
        'usuario__email',
        'celular',
        'telefone'
    ]
    
    list_editable = ['status']
    
    readonly_fields = ['usuario']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('usuario', 'status')
        }),
        ('Dados Pessoais/Jurídicos', {
            'fields': (
                'nome_completo', 
                'cpf', 
                'cnpj', 
                'rg_ie', 
                'emis_uf', 
                'nasc_fund', 
                'profis_cnae'
            )
        }),
        ('Endereço', {
            'fields': (
                'end_rua_av', 
                'end_numero', 
                'end_complem', 
                'end_bairro', 
                'end_cidade', 
                'end_estado', 
                'end_cep'
            )
        }),
        ('Contato', {
            'fields': ('telefone', 'celular')
        }),
        ('Propriedade', {
            'fields': ('propriedade', 'propr_cidade', 'propr_estado'),
            'classes': ('collapse',)
        }),
    )
    
    # Ações personalizadas
    actions = ['ativar_clientes', 'suspender_clientes', 'colocar_em_analise']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando um perfil existente
            return self.readonly_fields + ['cpf', 'cnpj']
        return self.readonly_fields

# Ações personalizadas
@admin.action(description='Ativar clientes selecionados')
def ativar_clientes(modeladmin, request, queryset):
    queryset.update(status='ativo')

@admin.action(description='Suspender clientes selecionados') 
def suspender_clientes(modeladmin, request, queryset):
    queryset.update(status='suspenso')

@admin.action(description='Colocar em análise')
def colocar_em_analise(modeladmin, request, queryset):
    queryset.update(status='analise')

# Adicionar as ações ao admin
PerfilClienteAdmin.actions = [ativar_clientes, suspender_clientes, colocar_em_analise]