from django.shortcuts import render
from plants.models import Plant

def index(request):
   
    latest_plants = Plant.objects.all().order_by('-id')[:3]

    return render(request, 'main/home.html', {
        "latest_plants": latest_plants
    })