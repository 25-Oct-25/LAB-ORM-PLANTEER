from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Plant
from .forms import PlantForm

# 1) Show all plants
def plants_view(request: HttpRequest):
    plants = Plant.objects.all().order_by('-created_at')
    return render(request, 'plants/all_plants.html', {"plants": plants})

# 2) Plant details
def plant_details_view(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    return render(request, 'plants/plant_detail.html', {"plant": plant})

# 3) Add plant
def add_plant_view(request: HttpRequest):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("plants:plants_view")
    else:
        form = PlantForm()

    return render(request, "plants/add_plant.html", {"form": form})

# 4) Update plant
def update_plant_view(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plants:plant_details_view", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/update_plant.html", {"form": form, "plant": plant})

# 5) Delete plant
def delete_plant(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect("plants:plants_view")

# 6) Search
def search_view(request: HttpRequest):
    query = request.GET.get("query", "")
    results = Plant.objects.filter(name__icontains=query) if query else []
    return render(request, "plants/search.html", {"query": query, "results": results})
