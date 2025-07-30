from django.contrib import admin
from django.contrib.auth.models import User
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
    
    # Remover readonly_fields para permitir seleção de usuário
    autocomplete_fields = ['usuario']
    
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
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando um perfil existente
            return ['cpf', 'cnpj']  # Removido 'usuario' para permitir alteração
        return []
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "usuario":
            # Mostrar apenas usuários que ainda não têm perfil
            usuarios_com_perfil = PerfilCliente.objects.values_list('usuario_id', flat=True)
            kwargs["queryset"] = User.objects.exclude(id__in=usuarios_com_perfil)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Configurar autocomplete para User
from django.contrib.auth.admin import UserAdmin
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = ['username', 'email', 'first_name', 'last_name']

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