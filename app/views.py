from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from datetime import datetime

def home(request):
    context = {
        'current_time': datetime.now()
    }
    return render(request, 'home.html', context)