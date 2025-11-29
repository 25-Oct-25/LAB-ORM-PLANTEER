from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.db import transaction


def sign_up(request):
    if request.method == "POST":

        try:
            with transaction.atomic():
                username = request.POST.get("username")
                password = request.POST.get("password")
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                email = request.POST.get("email")
                about = request.POST.get("about", "")
                avatar = request.FILES.get("avatar")

                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                new_user.save()
                

                profile = Profile(user=new_user, about=about)
                if avatar:
                    profile.avatar = avatar
                profile.save()

            messages.success(request, "Registered User Successfully")
            return redirect("accounts:sign_in")

        except Exception as e:
            print("Something went wrong:", e)

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


def user_profile_view(request, user_name):
    try:
        profile_user = User.objects.get(username=user_name)

        if not Profile.objects.filter(user=profile_user).exists():
            Profile.objects.create(user=profile_user)

        profile = Profile.objects.get(user=profile_user)

    except Exception as e:
        print("Error in user_profile_view:", e)
        messages.error(request, "Something went wrong, please try again.")
        return redirect("main:home")

 
    return render(request, 'accounts/profile.html', {
        "profile_user": profile_user,
        "profile": profile
    })




def my_reviews(request):
    return render(request, "accounts/my_reviews.html")

def update_user_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can update their profile.")
        return redirect("accounts:sign_in")

    user = request.user

    if request.method == "POST":
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.profile.about = request.POST.get("about")

        if request.FILES.get("avatar"):
            user.profile.avatar = request.FILES["avatar"]

        user.save()
        user.profile.save()
        messages.success(request, "Profile updated successfully!")

        return redirect("accounts:user_profile", user.username)

    return render(request, "accounts/update_profile.html", {"user": user})




