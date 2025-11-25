from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import ContactForm
from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            subject = f"New Contact Message from {first_name} {last_name} "
            full_message = f"From: {first_name} {last_name}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ["rs2success@gmail.com"],  
            )

            success = True
            form = ContactForm()  
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form, "success": success})



def contact_messages(request):
    msgs = ContactMessage.objects.all().order_by('-id')
    return render(request, "contact/contact_messages.html", {"messages": msgs})
