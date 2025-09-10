from django import forms
from .models import Banner, Logo, SiteSettings

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['titulo', 'imagem', 'link', 'ordem']

class LogoForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ['titulo', 'imagem', 'link', 'ordem']

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['email', 'telefone', 'facebook', 'instagram', 'youtube']