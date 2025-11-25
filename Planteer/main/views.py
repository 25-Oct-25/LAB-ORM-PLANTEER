
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from plant.models import Plant
from django.contrib import messages


# Create your views here.
def home_view(request: HttpRequest): 

    if request.user.is_authenticated:
        print(request.user.username)
    else:
        print("Anonymous User")

    
    #get all planter
    plant = Plant.objects.all()[:3]
    return render(request, 'main/home.html', {"plant" : plant})




