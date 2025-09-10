from django.contrib import admin
from .models import SiteSettings, Banner, Logo

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('email', 'telefone')

    def has_add_permission(self, request):
        # Garante que apenas uma instância de SiteSettings possa ser criada
        return not SiteSettings.objects.exists()

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem', 'link')
    ordering = ('ordem',)

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem', 'link')
    ordering = ('ordem',)