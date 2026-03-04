from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Case, When, Value, IntegerField
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
                  'lance_inicial', 'incremento_lance', 'parcela', 'lote', 'leilao', 'status']
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
            'lote': {
                'required': "O número do lote é obrigatório.",
            },
        }
        widgets = {
            # Define widgets if needed, e.g., for better UI
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leilao'].queryset = (
            Leilao.objects
            .filter(status__in=['ativo', 'inativo'])
            .annotate(
                ordem_status=Case(
                    When(status='ativo', then=Value(0)),
                    When(status='inativo', then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            )
            .order_by('ordem_status', 'id')
        )
    
    def clean(self):
        cleaned_data = super().clean()
        leilao = cleaned_data.get('leilao')
        lote = cleaned_data.get('lote')
        
        if leilao and lote:
            # Verificar se já existe outro cavalo com o mesmo lote neste leilão
            conflito = Cavalo.objects.filter(leilao=leilao, lote=lote)
            
            # Se estamos editando um cavalo existente, excluir ele da verificação
            if self.instance.pk:
                conflito = conflito.exclude(pk=self.instance.pk)
            
            if conflito.exists():
                cavalo_conflito = conflito.first()
                raise ValidationError({
                    'lote': f'O lote {lote} já está sendo usado pelo cavalo "{cavalo_conflito.nome}" neste leilão.'
                })
        
        return cleaned_data

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
