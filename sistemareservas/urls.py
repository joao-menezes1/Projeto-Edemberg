from django.urls import path
from . import views

urlpatterns = [
    path('eventos', views.evento_list, name='evento_list'),
    path('eventos/novo/', views.evento_create, name='evento_create'),
    path('eventos/<int:pk>/editar/', views.evento_update, name='evento_update'),
    path('eventos/<int:pk>/excluir/', views.evento_delete, name='evento_delete'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
