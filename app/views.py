from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from datetime import datetime

def home(request):
    context = {
        'current_time': datetime.now()
    }
    return render(request, 'home.html', context)

def clientes(request):
    return render(request, 'clientes.html')

def pedidos(request):
    return render(request, 'pedidos.html')