from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



def sign_up(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            new_user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            new_user.save()
            messages.success(request, "Registered User Successfully")

            return redirect("accounts:sign_in")

        except Exception as e:
            print(e)

    return render(request, "accounts/signup.html")

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect("main:home")  
        else:
            return render(request, "accounts/signin.html", {"error": "Invalid username or password"})

    return render(request, "accounts/signin.html")

def log_out(request):
    logout(request)
    return redirect("accounts:sign_in")