from django.shortcuts import render , redirect
from plants.models import Plant
from django.db.models import Count
from .forms import ContactForm
from .models import Contact



# Create your views here.

def home_view(request):

    plants = Plant.objects.order_by('-id')[:3]

    return render(request,'main/home.html',{'plants':plants})


def contact_page_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:contact_page_view')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})

def messages_page_view(request):
    messages = Contact.objects.all().order_by('-created_at')
    count = messages.count()   
    return render(request, 'main/messages.html', {
        'messages': messages,
        'count': count
    })

