from rest_framework import serializers
from .models import CategoriaEvento, Evento, Inscricao
from django.contrib.auth.models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaEvento
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):

    organizador = UserSerializer(read_only=True)
    categoria_nome = serializers.ReadOnlyField(source='categoria.nome')

    class Meta:
        model = Evento
        fields = [
            'id',
            'titulo',
            'descricao',
            'data',
            'local',
            'categoria',
            'categoria_nome',
            'organizador'
        ]

    def validate_data(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Não é possível criar evento no passado."
            )
        return value

class InscricaoSerializer(serializers.ModelSerializer):

    participante = UserSerializer(read_only=True)
    evento_detalhes = EventoSerializer(source='evento', read_only=True)

    class Meta:
        model = Inscricao
        fields = [
            'id',
            'participante',
            'evento',
            'evento_detalhes',
            'data_inscricao'
        ]
        read_only_fields = ['data_inscricao']
