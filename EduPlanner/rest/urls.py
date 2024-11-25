from django.urls import path, include
from rest_framework import routers
from .views import EventoViewSet, CalendarioViewSet

router = routers.DefaultRouter()

router.register('eventos', EventoViewSet)
router.register('calendario', CalendarioViewSet)

urlpatterns = [
    path('', include(router.urls))
]