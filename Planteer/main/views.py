from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages

from django.utils import timezone

from plants.models import Plant
from .models import Contact

# Create your views here.

def home_view(request:HttpRequest):

    plants = Plant.objects.all().order_by("-created_at")[0:3]

    return render(request, 'main/home.html', {"plants":plants})

def contact_view(request:HttpRequest):
    if request.method == "POST":
        contact = Contact(
            first_name=request.POST["first_name"], 
            last_name=request.POST["last_name"], 
            email=request.POST["email"], 
            message=request.POST["message"]
        )
        contact.save()

        email_context = {
            'name': f"{contact.first_name} {contact.last_name}",
            'subject': 'Contact Form Submission',
            'message': contact.message,
            'submission_date': contact.created_at.strftime("%B %d, %Y at %I:%M %p") if hasattr(contact, 'created_at') else timezone.now().strftime("%B %d, %Y at %I:%M %p"),
            'website_url': request.build_absolute_uri('/')
        }

        content_html = render_to_string('main/mail/confirmation.html', email_context)
        send_to = contact.email
        email_message = EmailMessage(
            'Thank You for Contacting Planteer',
            content_html, 
            settings.EMAIL_HOST_USER, 
            [send_to]
        )
        email_message.content_subtype = 'html'
        email_message.send()
        
        messages.success(request, "Your message is received. Thank You.", "alert-success")
        return redirect('main:contact_view')
    return render(request, 'main/contact_us.html')

def contact_meassages_view(request:HttpRequest):
    contact_messages = Contact.objects.all().order_by("-created_at")

    return render(request, 'main/contact_messages.html', {"contact_messages" : contact_messages} )