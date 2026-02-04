from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class CategoriaEvento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    #descricao = models.TextField()

    def __str__(self):
        return self.nome


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=200)
    categoria = models.ForeignKey(CategoriaEvento, on_delete=models.CASCADE)
    organizador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="eventos_criados"
    )

    def __str__(self):
        return self.titulo

    def usuario_inscrito(self, user):
        """Verifica se um usuário está inscrito neste evento"""
        return self.inscricao_set.filter(participante=user).exists()


class Inscricao(models.Model):
    participante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inscricoes"
    )
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participante', 'evento')
