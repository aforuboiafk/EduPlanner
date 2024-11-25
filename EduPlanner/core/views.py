from django.shortcuts import render
import calendar
from datetime import datetime

# Create your views here.

from django.shortcuts import render




def home(request):
    # Obtén el mes y año de los parámetros GET o usa el actual
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    
    # Genera la información del calendario
    cal = calendar.Calendar()
    days = cal.monthdayscalendar(year, month)  # Días organizados por semanas
    month_name = calendar.month_name[month]
    print(year, month,days)
    
    data = {
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