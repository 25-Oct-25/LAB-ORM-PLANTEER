from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Contact
from .forms import ContactForm

# Create your views here.
def contact_view(request:HttpRequest):
  if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact:contact_view')
  else:
    form = ContactForm()

  return render(request, 'contact/contact.html', {'form': form})


# Contact Us Messages page (admin or staff)
def contact_messages_view(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact/contact_messages.html', {'contacts': contacts})