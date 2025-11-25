from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from plants.models import Plant

def index_view(request):
    plants = Plant.objects.all().order_by('-created_at')[:3]
    return render(request, 'main/index.html', {'plants': plants})
