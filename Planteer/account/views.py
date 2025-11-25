from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def sign_up(request: HttpRequest):

    if request.method == "POST":
        try:
            new_user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                email=request.POST["email"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"]
            )

            new_user.save()

           
            messages.success(request, "Registered User Successfully")

            return redirect("account:sign_in")

        except Exception as e:
            print(e)
            messages.error(request, "Registration failed, please try again.")

    return render(request, "account/signup.html", {})



def sign_in(request: HttpRequest):

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"]
        )

        if user:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Your credentials are wrong, please try again")

    return render(request, "account/signin.html")



def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "Logged out successfully")

    return redirect(request.GET.get("next", "/"))
