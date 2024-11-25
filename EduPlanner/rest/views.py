from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from core.models import Evento
from .serializers import CalendarioSerializer, EventoSerializer
import requests

# Create your views here.
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class CalendarioViewSet(viewsets.ViewSet):
    def list(self, request):
        eventos = Evento.objects.all()

        feriados_response = requests.get("https://apis.digital.gob.cl/fl/feriados/2024")
        feriados = feriados_response.json()

        data = {
        'eventos': eventos,
        'feriados': feriados
        }

        serializer = CalendarioSerializer(data)

        return Response(serializer.data)