from django.shortcuts import render
from django.http import HttpRequest, HttpResponse



def index_view (request:HttpRequest):
    return render(request, 'main/index.html')
