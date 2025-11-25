from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout # اول وحده للتحقق من البيانات 
from django.contrib import messages




# Create your views here.


def sign_up(request: HttpRequest):

    if request.method == "POST":
        try:
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"]) # هذي الحقول موجوده اساسا في المودل حق اليوزر من جانقو وهذي الداله تشفر الباس  
            new_user.save()
            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect("accounts:sign_in")
        except Exception as e:
            print(e)
    

    return render(request, "accounts/signup.html", {})



def sign_in(request:HttpRequest):

    if request.method == "POST":

        #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"]) # اول شي يتحقق من المستخدم ثم ترجع يا يوزر او null  
        if user:
            #login the user تنشاء جلسه ان هذا المستخدم مسجل دخول 
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")



    return render(request, "accounts/signin.html")


def log_out(request: HttpRequest):

    logout(request) #تمسح الجلسه و بيانات الكوكيز 
    messages.success(request, "logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))
