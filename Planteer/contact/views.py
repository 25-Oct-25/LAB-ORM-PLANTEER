from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def contact_view (request:HttpRequest):
    return render(request, 'contact/contact.html')

def contact_messages(request:HttpRequest):
    return render(request, 'contact/contact_messages.html')

