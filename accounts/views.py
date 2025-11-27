from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout

# 1. Register View
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:home") # غيّر main:index لاسم الصفحة الرئيسية عندك
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# 2. Login View
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main:home") # غيّر main:index لاسم الصفحة الرئيسية عندك
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

# 3. Logout View
def logout_user(request):
    logout(request)
    return redirect("main:home") # غيّر accounts:home لاسم الصفحة الرئيسية عندك