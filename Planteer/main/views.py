from django.shortcuts import render, redirect
from plants.models import Plant
from .forms import ContactForm
from .models import Contact

def home(request):
    plants = Plant.objects.all()[:3]
    return render(request, 'main/home.html', {'plants': plants})

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

def contact_messages(request):
    messages = Contact.objects.all()
    return render(request, 'main/contact_messages.html', {'messages': messages})