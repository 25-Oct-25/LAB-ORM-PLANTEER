
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from plant.models import Plant


# Create your views here.
def home_view(request: HttpRequest): 
    
    #get all planter
    plant = Plant.objects.all()[:3]
    return render(request, 'main/home.html', {"plant" : plant})




