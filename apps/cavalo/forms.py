from django import forms

from apps.leilao.models import Leilao
from .models import Cavalo, Foto, Video

class CavaloForm(forms.ModelForm):
    class Meta:
        model = Cavalo
        fields = ['nome', 'raca', 'descricao', 'registro',
                  'nascimento', 'geracao', 'altura', 'sexo', 'pelagem',
                  'criador', 'vendedor', 'alojamento', 'pai', 'mae',
                  'avo_paterno', 'avo_paterna', 'avo_materno', 'avo_materna',
                  'bisavo_paterno1', 'bisavo_paterno2', 'bisavo_paterno3', 'bisavo_paterno4',
                  'bisavo_materno1', 'bisavo_materno2', 'bisavo_materno3', 'bisavo_materno4',
                  'lance_inicial', 'incremento_lance', 'parcela', 'leilao', 'status']
        help_texts = {
            # Add any specific help texts if needed
        }
        error_messages = {
            'nome': {
                'max_length': "O nome do cavalo é muito longo.",
            },
            'registro': {
                'unique': "Já existe um cavalo com este registro.",
            },
        }
        widgets = {
            # Define widgets if needed, e.g., for better UI
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas leilões com status 'aberto'
        self.fields['leilao'].queryset = Leilao.objects.filter(status='ativo')

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['cavalo', 'url_youtube', 'legenda']

class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['cavalo', 'imagem', 'is_destaque', 'ordem']
        widgets = {
            'ordem': forms.HiddenInput(),
        }
