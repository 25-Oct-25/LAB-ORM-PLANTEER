from django.shortcuts import render, redirect
from .models import Plant
from .forms import PlantForm

def all_plants(request):
    category = request.GET.get("category")
    edible = request.GET.get("is_edible")

    plants = Plant.objects.all()

    # filter by category
    if category and category != "all":
        plants = plants.filter(category=category)

    # filter by edibility
    if edible == "true":
        plants = plants.filter(is_edible=True)
    elif edible == "false":
        plants = plants.filter(is_edible=False)

    return render(request, 'plants/all_plants.html', {"plants": plants})

def plant_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    return render(request, 'plants/plant_detail.html', {
        "plant": plant,
        "related_plants": related_plants
    })

def create_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/plants/all/')
    else:
        form = PlantForm()

    return render(request, 'plants/create_plant.html', {"form": form})

def update_plant(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect(f'/plants/{plant.id}/detail/')
    else:
        form = PlantForm(instance=plant)

    return render(request, 'plants/update_plant.html', {"form": form})

def delete_plant(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    plant.delete()
    return redirect('/plants/all/')

def search_plants(request):
    query = request.GET.get("q", "")
    plants = Plant.objects.filter(name__contains=query)

    return render(request, 'plants/search.html', {
        "plants": plants,
        "query": query
    })
