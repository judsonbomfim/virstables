from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'resumo', 'imagem', 'conteudo', 'published']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumo': forms.TextInput(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'published': forms.Select(choices=[(True, 'Sim'), (False, 'Não')], attrs={'class': 'form-control'}),
        }