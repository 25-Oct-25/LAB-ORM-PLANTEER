from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from plants.models import Plant

# Create your views here.

def home_view(request:HttpRequest):

    plant = Plant.objects.all().order_by("-created_at")[0:3]

    return render(request, 'main/home.html', {"plant":plant})

def contact_view(request:HttpRequest):
    return render(request, 'main/contact_us.html')

def contact_meassages_view(request:HttpRequest):
    return render(request, 'main/contact_meassages.html')