from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('eventos', views.evento_list, name='evento_list'),
    path('eventos/novo/', views.evento_create, name='evento_create'),
    path('categorias/novo/', views.categoria_create, name='categoria_create'),
    path('eventos/<int:pk>/editar/', views.evento_update, name='evento_update'),
    path('eventos/<int:pk>/excluir/', views.evento_delete, name='evento_delete'),
    path('eventos/<int:pk>/inscritos/', views.evento_inscritos, name='evento_inscritos'),
    path('eventos/<int:pk>/inscrever/', views.inscricao_criar, name='inscricao_criar'),
    path('eventos/<int:pk>/desinscrever/', views.inscricao_cancelar, name='inscricao_cancelar'),
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/novo/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/excluir/', views.categoria_delete, name='categoria_delete'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('minhas_inscricoes/',views.minhas_inscricoes,name='minhas_inscricoes'),
    path('api/', include('sistemareservas.api_urls')),  # Inclui as URLs da API


]
