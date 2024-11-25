from core.models import Evento, Feriado
from rest_framework import routers, serializers

class EventoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='titulo', max_length=255)
    fecha_inicio = serializers.DateTimeField(source='fecha_inicio')
    fecha_fin = serializers.DateTimeField(source='fecha_fin')
    tipo = serializers.CharField(max_length=100)

class FeriadoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=255)
    fecha = serializers.DateField()
    tipo = serializers.CharField(max_length=100)

class CalendarioSerializer(serializers.Serializer):
    eventos = EventoSerializer(many=True)
    feriados = FeriadoSerializer(many=True)