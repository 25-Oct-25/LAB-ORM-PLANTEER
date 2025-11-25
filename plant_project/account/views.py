from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def sign_up(request: HttpRequest):

    if request.method == "POST":

        print("POST WORKING")  # للتأكد أن الفورم يشتغل

        try:
            password = request.POST.get("password")
            confirm = request.POST.get("confirm_password")

            if password != confirm:
                messages.error(request, "Passwords do not match", "alert-danger")
                return redirect("account:signup")

            new_user = User.objects.create_user(
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                password=password
            )
            new_user.save()

            messages.success(request, "Registered user succesfuly", "alert-success")

            # بعد التسجيل نرسل المستخدم لصفحة تسجيل الدخول
            return redirect("account:signin")

        except Exception as e:
            print("Error:", e)

    return render(request, "account/signup.html")


def sign_in(request: HttpRequest):

    if request.method == "POST":
        
        username = request.POST.get("username")
        password = request.POST.get("password")

        #  authenticate للتحقق من صحة المعلومات
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #  تسجيل الجلسة session login
            login(request, user)

            messages.success(request, "Logged in successfully!", "alert-success")

            #  تحويل للصفحة الرئيسيm
            return redirect("main:index")
        
        else:
            #  اذا فشل تسجيل الدخول
            messages.error(request, "Invalid username or password", "alert-danger")
            return redirect("account:signin")

    return render(request, "account/signin.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully", "alert-success")
    return redirect("main:index")  




