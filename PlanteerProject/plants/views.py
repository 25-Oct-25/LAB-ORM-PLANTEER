from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment

# Create your views here.


def all_plants(request):
    category = request.GET.get("category")
    edible = request.GET.get("edible")

    plants = Plant.objects.all()

    if category:
        plants = plants.filter(category=category)

    if edible == "true":
        plants = plants.filter(is_edible=True)

    context = {"plants": plants}
    return render(request, "plants/all_plants.html", context)


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    related = Plant.objects.filter(category=plant.category).exclude(id=plant_id)

    if request.method == "POST":
        Comment.objects.create(
            plant=plant,
            full_name=request.POST["full_name"],
            content=request.POST["content"],
        )
        return redirect("plant_detail", plant_id=plant_id)

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related": related,
        "comments": plant.comments.all()
    })


def add_plant(request):
    if request.method == "POST":
        Plant.objects.create(
            name=request.POST["name"],
            about=request.POST["about"],
            used_for=request.POST["used_for"],
            category=request.POST["category"],
            is_edible=("is_edible" in request.POST),
            image=request.FILES["image"]
        )
        return redirect("all_plants")
    return render(request, "plants/add_plant.html")


def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.category = request.POST["category"]
        plant.is_edible = ("is_edible" in request.POST)
        if "image" in request.FILES:
            plant.image = request.FILES["image"]
        plant.save()
        return redirect("plant_detail", plant_id=plant.id)

    return render(request, "plants/update_plant.html", {"plant": plant})


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect("all_plants")


def search_plants(request):
    q = request.GET.get("q", "")
    plants = Plant.objects.filter(name__icontains=q)
    return render(request, "plants/search.html", {"plants": plants, "q": q})
