from django.db import migrations

def create_default_sitesettings(apps, schema_editor):
    SiteSettings = apps.get_model('site_config', 'SiteSettings')
    if not SiteSettings.objects.exists():
        SiteSettings.objects.create(
            email='contato@seudominio.com',
            telefone='(00) 00000-0000',
            facebook='',
            instagram='',
            youtube=''
        )

class Migration(migrations.Migration):

    dependencies = [
        ('site_config', '0002_banner_logo'),
    ]

    operations = [
        migrations.RunPython(create_default_sitesettings),
    ]