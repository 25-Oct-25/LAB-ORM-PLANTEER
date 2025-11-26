from django.shortcuts import render
from plants.models import Plant
from .models import ContactMessage
from django.db.models import Count
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def home_view(request):
    plants = Plant.objects.all().annotate(countries_count=Count("Countries")).order_by('-created_at')[:3]
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
        
        content_html = render_to_string("main/mail/confirmation.html")
        send_to=email
        email_message = EmailMessage(
            "Confirmation",            
            content_html,               
            settings.EMAIL_HOST_USER,   
            [send_to]                 
        )
        email_message.content_subtype = "html"  
        email_message.send()  
        return render(request, "main/contact.html", {"success": True})

    return render(request, "main/contact.html")


def contact_messages_view(request):
    messages = ContactMessage.objects.all().order_by('-sent_at')
    return render(request, "main/contact_messages.html", {"messages": messages})
