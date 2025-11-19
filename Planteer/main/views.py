from django.shortcuts import render
from plants.models import Plant
from .models import ContactMessage



def home_view(request):
    plants = Plant.objects.all().order_by('-created_at')[:3]
    return render(request, "main/home.html", {"plants": plants})


def contact_view(request):
    if request.method == "POST":
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        email = request.POST.get("email")
        msg = request.POST.get("message")

        ContactMessage.objects.create(
            first_name=first,
            last_name=last,
            email=email,
            message=msg
        )
        return render(request, "main/contact.html", {"success": True})

    return render(request, "main/contact.html")


def contact_messages_view(request):
    messages = ContactMessage.objects.all().order_by('-sent_at')
    return render(request, "main/contact_messages.html", {"messages": messages})
