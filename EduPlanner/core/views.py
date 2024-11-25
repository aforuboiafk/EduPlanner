from django.shortcuts import render, redirect, get_object_or_404
import calendar, requests
from datetime import datetime, date
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Evento

# Create your views here.
TIPOS_EVENTOS = [
    "Inicio de Semestre",
    "Fin de Semestre",
    "Inicio de Inscripción de Asignaturas",
    "Fin de Inscripción de Asignaturas",
    "Receso Académico",
    "Feriado Nacional",
    "Feriado Regional",
    "Inicio de Plazos de Solicitudes Administrativas",
    "Fin de Plazos de Solicitudes Administrativas",
    "Inicio de Plazos para la Gestión de Beneficio",
    "Fin de Plazos para la Gestión de Beneficios",
    "Ceremonia de Titulación o Graduación",
    "Reunión de Consejo Académico",
    "Talleres y Charlas",
    "Día de Orientación para Nuevos Estudiantes",
    "Eventos Extracurriculares",
    "Inicio de Clases",
    "Último Día de Clases",
    "Día de Puertas Abiertas",
    "Suspensión de Actividades Completa",
    "Suspensión de Actividades Parcial",
]


def home(request):
    eventos = Evento.objects.all()

    tipos = []

    fecha_info = {}
    # Obtén el mes y año de los parámetros GET o usa el actual
    year = int(request.GET.get("year", datetime.now().year))
    month = int(request.GET.get("month", datetime.now().month))
    filtro = request.GET.get("filtro")
    mes_info = request.GET.get("mes")
    dia_info = request.GET.get("dia")
    año_info = request.GET.get("año")
    if dia_info and mes_info and año_info:
        fecha_info = {"dia": int(dia_info), "mes": int(mes_info), "año": int(año_info)}
    year_s = str(year)
    month_s = str(month)
    # Genera la información del calendario
    cal = calendar.Calendar()
    days = cal.monthdayscalendar(year, month)  # Días organizados por semanas
    month_name = calendar.month_name[month]
    grupos = [grupo.name for grupo in request.user.groups.all()]

    calendario_response = requests.get("http://127.0.0.1:8000/api/calendario/")
    if calendario_response.status_code == 200:
        calendario = calendario_response.json()
        for evento in calendario["eventos"]:
            evento["fecha_inicio"] = evento["fecha_inicio"].split("T")[0].split("-")
            evento["fecha_inicio"] = {
                "dia": int(evento["fecha_inicio"][2]),
                "mes": int(evento["fecha_inicio"][1]),
                "año": int(evento["fecha_inicio"][0]),
            }
            evento["fecha_fin"] = evento["fecha_fin"].split("T")[0].split("-")
            evento["fecha_fin"] = {
                "dia": int(evento["fecha_fin"][2]),
                "mes": int(evento["fecha_fin"][1]),
                "año": int(evento["fecha_fin"][0]),
            }
            if evento["tipo"] not in tipos and evento["aprobado"]:
                if filtro:
                    if evento["tipo"] == filtro:
                        tipos.append(evento["tipo"])
                else:
                    tipos.append(evento["tipo"])

    else:
        calendario = []

    data = {
        "tipo_filtro": filtro,
        "grupos": grupos,
        "fecha_info": fecha_info,
        "filtr": tipos,
        "year_s": year_s,
        "mont_s": month_s,
        "calendario": calendario,
        "tipos": TIPOS_EVENTOS,
        "eventos": eventos,
        "permisos": True,
        "days": days,
        "month": month,
        "year": year,
        "month_name": month_name,
        "prev_month": month - 1 if month > 1 else 12,
        "next_month": month + 1 if month < 12 else 1,
        "prev_year": year - 1 if month == 1 else year,
        "next_year": year + 1 if month == 12 else year,
    }

    return render(request, "core\home.html", data)


def crear_evento(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        tipo = request.POST.get("tipo")

        # Crear el nuevo evento
        evento = Evento(
            titulo=titulo,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo=tipo,
        )
        evento.save()
        return redirect("/")  # Redirige a la lista de eventos, puedes cambiar esta URL


def modificar_evento(request):

    if request.method == "POST":
        evento_id = request.POST["evento_id"]
        evento = Evento.objects.get(id=evento_id)

        # Actualizar los campos del evento
        evento.titulo = request.POST["titulo"]
        evento.descripcion = request.POST["descripcion"]
        evento.fecha_inicio = request.POST["fecha_inicio"]
        evento.fecha_fin = request.POST["fecha_fin"]
        evento.tipo = request.POST["tipo"]
        evento.aprobado = request.POST['aprobado']
        evento.save()  # Guardar cambios
        return redirect("/")  # Redirigir a la lista de eventos
    else:
        return render(request, "")


def eliminar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.delete()  # Eliminar evento
    return redirect("/")  # Redirigir a la lista de eventos


def modificar(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    data = {"tipos": TIPOS_EVENTOS, "evento": evento}

    return render(request, "core/modificar.html", data)


def login(request):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        contraseña = request.POST["contraseña"]

        usuario_final = User.objects.filter(username=usuario).first()

        if not usuario_final:
            messages.error(request, "El usuario no existe")

            return render(request, "core/login.html")

        if usuario_final.check_password(contraseña):
            auth_login(request, usuario_final)
            return redirect("/")

        else:
            messages.error(request, "El usuario no existe")
            return render(request, "core/login.html")

    return render(request, "core/login.html")


def cerrar_sesion(request):
    logout(request)
    return redirect("/")
