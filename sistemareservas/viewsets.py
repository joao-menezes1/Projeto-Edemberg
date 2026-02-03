from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Evento, CategoriaEvento, Inscricao
from .serializers import EventoSerializer, CategoriaSerializer, InscricaoSerializer

from rest_framework import permissions


class IsOrganizador(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH', 'DELETE', 'POST']:
            return (
                request.user.is_authenticated and
                request.user.groups.filter(name='organizadores').exists()
            )

        return False

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all().order_by('data')
    serializer_class = EventoSerializer
    permission_classes = [IsOrganizador]

    def perform_create(self, serializer):
        serializer.save(organizador=self.request.user)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = CategoriaEvento.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizador]

class InscricaoViewSet(viewsets.ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Inscricao.objects.filter(participante=self.request.user)

    def perform_create(self, serializer):
        serializer.save(participante=self.request.user)
