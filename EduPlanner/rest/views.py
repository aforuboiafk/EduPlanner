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

        eventos_data = EventoSerializer(eventos, many=True).data

        try:
            feriados_response = requests.get(
                "https://apis.digital.gob.cl/fl/feriados/2024", timeout=10
            )
            feriados_response.raise_for_status()
            feriados = feriados_response.json()
        except requests.exceptions.RequestException:
            feriados = []

        data = {"eventos": eventos, "feriados": feriados}

        serializer = CalendarioSerializer(data)

        return Response(serializer.data)
