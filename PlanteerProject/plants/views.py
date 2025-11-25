from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Plant, Comment, Country


# ---------------------------------------------------------
# Helper: Check if user is admin
# ---------------------------------------------------------
def is_admin(user):
    return user.is_staff


# ---------------------------------------------------------
#_SIGNUP
# ---------------------------------------------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "auth/signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "auth/signup.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect("/")

    return render(request, "auth/signup.html")


# ---------------------------------------------------------
#_LOGIN
# ---------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "auth/login.html", {"error": "Invalid username or password"})

    return render(request, "auth/login.html")


# ---------------------------------------------------------
#_LOGOUT
# ---------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect("/")


# ---------------------------------------------------------
# ALL PLANTS
# ---------------------------------------------------------
def all_plants(request):
    q = request.GET.get("q", "")
    category = request.GET.get("category")
    edible = request.GET.get("edible")
    countries_filter = request.GET.getlist("countries[]")

    plants = Plant.objects.all()
    countries = Country.objects.all()

    if q:
        plants = plants.filter(name__icontains=q)

    if category:
        plants = plants.filter(category=category)

    if edible == "true":
        plants = plants.filter(is_edible=True)

    if countries_filter:
        plants = plants.filter(countries__id__in=countries_filter).distinct()

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "countries": countries,
        "selected_countries": countries_filter,
    })


# ---------------------------------------------------------
# PLANT DETAIL + COMMENTS
# ---------------------------------------------------------
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    related = Plant.objects.filter(category=plant.category).exclude(id=plant_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/login/")

        Comment.objects.create(
            plant=plant,
            full_name=request.user.username,
            content=request.POST["content"],
        )

        return redirect("plant_detail", plant_id=plant_id)

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related": related,
        "comments": plant.comments.all()
    })


# ---------------------------------------------------------
# ADD PLANT (Admin only)
# ---------------------------------------------------------
@user_passes_test(is_admin, login_url="/login/")
def add_plant(request):
    countries = Country.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        about = request.POST.get("about")
        used_for = request.POST.get("used_for")
        category = request.POST.get("category")
        edible = True if request.POST.get("is_edible") == "on" else False
        image = request.FILES.get("image")

        plant = Plant.objects.create(
            name=name,
            about=about,
            used_for=used_for,
            category=category,
            is_edible=edible,
            image=image
        )

        countries_ids = request.POST.getlist("countries[]")
        plant.countries.set(countries_ids)

        return redirect("all_plants")

    return render(request, "plants/add_plant.html", {
        "countries": countries
    })


# ---------------------------------------------------------
# UPDATE PLANT (Admin only)
# ---------------------------------------------------------
@user_passes_test(is_admin, login_url="/login/")
def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    countries = Country.objects.all()
    selected_countries = plant.countries.values_list("id", flat=True)

    if request.method == "POST":
        plant.name = request.POST.get("name")
        plant.about = request.POST.get("about")
        plant.used_for = request.POST.get("used_for")
        plant.category = request.POST.get("category")
        plant.is_edible = True if request.POST.get("is_edible") == "on" else False

        if request.FILES.get("image"):
            plant.image = request.FILES.get("image")

        plant.save()

        countries_ids = request.POST.getlist("countries[]")
        plant.countries.set(countries_ids)

        return redirect("plant_detail", plant_id=plant.id)

    return render(request, "plants/update_plant.html", {
        "plant": plant,
        "countries": countries,
        "selected_countries": list(selected_countries)
    })


# ---------------------------------------------------------
# DELETE PLANT (Admin only)
# ---------------------------------------------------------
@user_passes_test(is_admin, login_url="/login/")
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect("all_plants")


# ---------------------------------------------------------
# SEARCH PAGE
# ---------------------------------------------------------
def search_plants(request):
    q = request.GET.get("q", "")
    category = request.GET.get("category", "")
    edible = request.GET.get("edible", "")
    countries_filter = request.GET.getlist("countries[]")

    plants = Plant.objects.all()

    if q:
        plants = plants.filter(name__icontains=q)

    if category:
        plants = plants.filter(category=category)

    if edible == "true":
        plants = plants.filter(is_edible=True)
    elif edible == "false":
        plants = plants.filter(is_edible=False)

    if countries_filter:
        plants = plants.filter(countries__id__in=countries_filter).distinct()

    countries = Country.objects.all()

    return render(request, "plants/search.html", {
        "plants": plants,
        "countries": countries,
        "selected_countries": countries_filter,
        "q": q
    })


# ---------------------------------------------------------
# FILTER BY COUNTRY PAGE
# ---------------------------------------------------------
def plants_by_country(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    plants = Plant.objects.filter(countries__id=country_id)

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "current_country": country
    })
