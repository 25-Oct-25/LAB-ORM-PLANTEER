from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
# Sign Up View
def sign_up(request: HttpRequest):

    if request.method == "POST":

        try:
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            new_user.save()
            messages.success(request, "Requested User Successfully", "alert-success")
            return redirect('accounts:sign_in')
        except Exception as e:
            print(e)
                

    return render(request, 'accounts/signup.html')

# Login View
def sign_in(request: HttpRequest):

    if request.method == "POST":
        #check user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user:
            #login the user
            login(request, user)          
            messages.success(request, "Logged in Successfully", "alert-success")
            return redirect('main:home_view')
        else:
            messages.error(request, "Please enter valid credentials, Try again ..", "alert-danger")

    return render(request, 'accounts/signin.html')

# Logout View
def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "Logged out Successfully", "alert-warning")

    return redirect('main:home_view')