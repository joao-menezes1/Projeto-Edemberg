from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

from .models import Evento, CategoriaEvento, Inscricao
from .serializers import EventoSerializer, CategoriaSerializer, InscricaoSerializer

from rest_framework import permissions

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_login_view(request):
    """Endpoint de login exclusivo para a API"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Usuário e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'id': user.id,
            'username': user.username,
            'is_organizador': user.groups.filter(name='organizadores').exists()
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


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
