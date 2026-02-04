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

    def validate_nome(self, value):
        if CategoriaEvento.objects.filter(nome__iexact=value).exists():
            raise serializers.ValidationError(
                'Já existe uma categoria com esse nome.'
            )
        return value

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

    def validate(self, data):
        if not data.get('titulo'):
            raise serializers.ValidationError(
                'Título é obrigatório.'
            )
        if not data.get('local'):
            raise serializers.ValidationError(
                'Local é obrigatório.'
            )
        return data
    
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

    def validate(self, data):
        user = self.context['request'].user
        evento = data.get('evento')

        if Inscricao.objects.filter(
            participante=user,
            evento=evento
        ).exists():
            raise serializers.ValidationError(
                "Você já está inscrito neste evento."
            )
        return data

