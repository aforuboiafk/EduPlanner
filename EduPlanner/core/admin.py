from django.contrib import admin
from .models import Evento, Feriado

# Register your models here.

admin.site.register(Evento)
admin.site.register(Feriado)
