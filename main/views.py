from django.shortcuts import render
from plants.models import Plant

def home(request):
    plants = Plant.objects.all()[:3]
    return render(request, 'home.html', {"plants": plants})
