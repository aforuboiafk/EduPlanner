from core.models import Evento, Feriado
from rest_framework import routers, serializers


class EventoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source="titulo", max_length=255)
    fecha_inicio = serializers.DateTimeField()
    fecha_fin = serializers.DateTimeField()
    tipo = serializers.CharField(max_length=100)

    class Meta:
        model = Evento
        fields = ["nombre", "fecha_inicio", "fecha_fin", "tipo", "aprobado"]


class FeriadoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=255)
    fecha = serializers.DateField()
    tipo = serializers.CharField(max_length=100)


class CalendarioSerializer(serializers.Serializer):
    eventos = EventoSerializer(many=True)
    feriados = FeriadoSerializer(many=True)
