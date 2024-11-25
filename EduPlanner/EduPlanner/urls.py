"""
URL configuration for EduPlanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core.views import (
    home,
    login,
    modificar_evento,
    eliminar_evento,
    crear_evento,
    modificar,
    cerrar_sesion,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("api/", include("rest.urls")),
    path("login/", login, name="login"),
    path("logout/", cerrar_sesion, name="logout"),
    path("crear_evento/", crear_evento, name="crear_evento"),
    path("modificar/<int:evento_id>/", modificar, name="modificar"),
    path("modificar_evento/", modificar_evento, name="modificar_evento"),
    path("eliminar_evento/<int:evento_id>/", eliminar_evento, name="eliminar_evento"),
]
