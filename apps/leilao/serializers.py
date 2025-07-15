from rest_framework import serializers
from core.models import Cavalo, Leilao, Lance

class CavaloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cavalo
        fields = ['id', 'nome', 'raca', 'idade', 'vendedor']

class LeilaoSerializer(serializers.ModelSerializer):
    cavalo = CavaloSerializer(read_only=True)
    class Meta:
        model = Leilao
        fields = ['id', 'cavalo', 'data_inicio', 'data_fim', 'lance_inicial', 'status']

class LanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lance
        fields = ['id', 'leilao', 'usuario', 'valor', 'data']