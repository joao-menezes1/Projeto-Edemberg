from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import login_view
from .viewsets import EventoViewSet, CategoriaViewSet, InscricaoViewSet

router = SimpleRouter()
# Registrando as rotas da sua aplicação
router.register(r'categorias', CategoriaViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'inscricoes', InscricaoViewSet)

app_name = 'api'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
]