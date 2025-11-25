from datetime import datetime
from django.shortcuts import redirect, render
from django.http import HttpRequest
from plant.models import Plant
from .models import Contact
# Create your views here.

def home_view(request:HttpRequest):
    
    if request.user.is_authenticated:
        print(request.user.email)
    else:
        print("User is not logged in")

    plants = Plant.objects.all().order_by('-created_at')[0:3]
    return render(request, 'main/home.html', {"plants":plants} )

def contact_view(request: HttpRequest):
    
    if request.method == "POST":
        new_contact = Contact(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            message=request.POST["message"],

        )
        new_contact.save()

    return render(request, "main/contact.html" )

def contact_messages_view(request):

    contacts = Contact.objects.all()


    return render(request, "main/contact_messages.html" , { "contacts" : contacts} )
     
def delete_all_contacts(request):
    Contact.objects.all().delete()
    return redirect("main:contact_messages_view")
     