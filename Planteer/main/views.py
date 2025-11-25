from django.shortcuts import render
from django.http import HttpRequest
from plant.models import Plant
# Create your views here.

def home_view(request:HttpRequest):
    if request.user.is_authenticated:
        print(request.user.username)
    plants=Plant.objects.all()[0:3]
    return render(request,"main/home.html",{"plants":plants})