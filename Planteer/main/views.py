from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from plants.models import Plant
from .models import Contact
from .forms import ContactForm

def home_view(request):
    """
    Displays the homepage with the latest 6 added plants.
    """
    recent_plants = Plant.objects.all().order_by('-created_at')[:6] 
    
    context = {
        'recent_plants': recent_plants,
        'page_title': 'Home Page',
    }
    return render(request, 'main/home.html', context)


def contact_us_view(request):
    """
    Handles the contact form and saves the messages in the database.
    """
    from .forms import ContactForm 
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully! Thank you for contacting us.")
            
            return redirect('main:contact_us') 
    else:
        form = ContactForm()
    
    context = {'form': form, 'page_title': 'Contact Us'}
    return render(request, 'main/contact_form.html', context)

def contact_messages_view(request):
    """
    Displays all contact messages. (Should be secured for admins later)
    """
    contact_messages = Contact.objects.all().order_by('-created_at')
    
    context = {
        'messages': contact_messages,
        'page_title': 'User Messages',
    }
    return render(request, 'main/contact_messages.html', context)

def contact_messages_view(request):
    return render(request, 'main/contact_messages.html', {'messages': []})
