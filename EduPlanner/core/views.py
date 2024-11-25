from django.shortcuts import render, redirect
import calendar
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Evento
# Create your views here.





def home(request):
    eventos = Evento.objects.all()
    
    
    # Obtén el mes y año de los parámetros GET o usa el actual
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    
    # Genera la información del calendario
    cal = calendar.Calendar()
    days = cal.monthdayscalendar(year, month)  # Días organizados por semanas
    month_name = calendar.month_name[month]
    print(year, month,days)
    
    data = {
        'eventos':eventos,
        'permisos':True, 
        'days': days,
        'month': month,
        'year': year,
        'month_name': month_name,
        'prev_month': month - 1 if month > 1 else 12,
        'next_month': month + 1 if month < 12 else 1,
        'prev_year': year - 1 if month == 1 else year,
        'next_year': year + 1 if month == 12 else year,
    }



    return render(request, 'core\home.html', data)



def modificar_evento(request):
    if request.method == 'POST':
        evento_id = request.POST['evento_id']
        evento = Evento.objects.get(id=evento_id)

        # Actualizar los campos del evento
        evento.titulo = request.POST['titulo']
        evento.descripcion = request.POST['descripcion']
        evento.fecha_inicio = request.POST['fecha_inicio']
        evento.fecha_fin = request.POST['fecha_fin']
        evento.tipo = request.POST['tipo']
        evento.aprobado = request.POST['aprobado'] == 'True'

        evento.save()  # Guardar cambios
        return redirect('/')  # Redirigir a la lista de eventos
    

def eliminar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.delete()  # Eliminar evento
    return redirect('/')  # Redirigir a la lista de eventos


def login(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        contraseña = request.POST['contraseña']

        usuario_final = User.objects.filter(username=usuario).first()
        
        if not usuario_final:
            messages.error(request, "El usuario no existe")
            return render(request,'core/login.html')


        if usuario_final.check_password(contraseña):    
            login(request, usuario_final)
            print(usuario_final)
            print('todo weno')
            return redirect('/')
        
        else:
            messages.error(request,"El usuario no existe")
            return render(request,'core/login.html')

    return render(request,'core/login.html')