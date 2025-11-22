from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from plants.models import Plant


# Create your views here.
def home_view(request:HttpRequest):

    #get all plants
    plants = Plant.objects.all()[0:3]

    return render(request, 'main/home.html', {"plants": plants})

