from django.shortcuts import render, redirect
from django.http import HttpRequest
from plant.models import Plant
from .models import Contact
# Create your views here.

def home(request: HttpRequest):
    plants = Plant.objects.all().order_by('?')[:3]
    return render(request, "main/home.html", {"plants": plants})


def contact_us(request: HttpRequest):
    if request.method == "POST":
        new_contact = Contact(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        new_contact.save()
        return redirect('main:home')
    
    return render(request, "main/contact.html")

def contact_messages(request: HttpRequest):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, "main/messages.html", {"messages": messages})