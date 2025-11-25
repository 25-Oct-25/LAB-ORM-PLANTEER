from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages


# Create your views here.


def signin_view (request:HttpRequest):
    if request.method =="POST":
        user= authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user:
            login(request,user)
            messages.success(request,"Logged in successfully", "alert-success")
            return redirect(request.GET.get("next",'/'))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-wrong")

    return render(request,"accounts/signin.html",{})


def signup_view (request:HttpRequest):
    if request.method =="POST":
        try:
            new_user =User.objects.create_user(username=request.POST["username"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=request.POST["password"])
            new_user.save()
            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect("accounts:signup_view")
        except Exception as e:
            print(e)    

    return render(request,"accounts/signup.html",{})

def logout_view (request:HttpRequest):
    logout(request)

    return redirect(request.GET.get("next","/"))