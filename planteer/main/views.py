from django.shortcuts import render, redirect
from plants.models import Plant
from .models import Contact
from .forms import ContactForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


# Create your views here.

def home_view(request):
    latest_plants = Plant.objects.order_by('-created_at')[:3]
    return render(request, 'main/home.html', {
        'latest_plants': latest_plants
    })


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect('main:contact')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {
        'form': form
    })



def contact_messages_view(request):
    messages = Contact.objects.order_by('-created_at')
    return render(request, 'main/contact_messages.html', {
        'messages': messages
    })

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created. Welcome!")
            return redirect('main:home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")

            if next_url:
                return redirect(next_url)
            return redirect('main:home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm(request)

    return render(request, 'main/login.html', {
        'form': form,
        'next': next_url,
    })


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('main:home')



def admin_only(user):
    return user.is_superuser

@user_passes_test(admin_only)
def contact_messages_view(request):
    messages = Contact.objects.order_by('-created_at')
    return render(request, 'main/contact_messages.html', {
        'messages': messages
    })
