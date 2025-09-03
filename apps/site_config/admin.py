from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('email', 'telefone')

    def has_add_permission(self, request):
        # Garante que apenas uma instância de SiteSettings possa ser criada
        return not SiteSettings.objects.exists()

# Register your models here.