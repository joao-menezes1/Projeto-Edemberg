from django.contrib import admin
from .models import CategoriaEvento, Evento, Inscricao

# Register your models here.

admin.site.register(CategoriaEvento)
admin.site.register(Evento)
admin.site.register(Inscricao)