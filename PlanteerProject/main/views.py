from django.shortcuts import render, redirect
from .models import Contact
from plants.models import Plant

# Create your views here.

def home(request):
    plants = Plant.objects.all()[:3]
    return render(request, "main/home.html", {"plants": plants})



def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            message=request.POST["message"],
        )
        return redirect("contact")

    return render(request, "main/contact.html")


def contact_messages(request):
    messages = Contact.objects.all().order_by("-created_at")
    return render(request, "main/contact_messages.html", {"messages": messages})
