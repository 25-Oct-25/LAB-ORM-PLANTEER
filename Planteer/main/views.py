from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from plants.models import Plant
from .models import Contact
from .forms import ContactForm


def home_view(request):
    recent_plants = Plant.objects.all().order_by('-created_at')[:6] 
    context = {
        'recent_plants': recent_plants, 
        'page_title': 'Home Feed'
    }
    return render(request, 'main/home.html', context)


def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully. Thank you!')
            return redirect('main:contact_us') 
    else:
        form = ContactForm()
    
    context = {'form': form, 'page_title': 'Contact Us'}
    return render(request, 'main/contact_form.html', context)


def contact_messages_view(request):
    contact_messages = Contact.objects.all().order_by('-created_at')
    context = {
        'messages': contact_messages,
        'page_title': 'User Messages',
    }
    return render(request, 'main/contact_messages.html', context)
