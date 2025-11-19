from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Plant
from .forms import PlantForm

# Create your views here.

def all_plants(request: HttpRequest):
    plants = Plant.objects.all()
    
    cat_filter = request.GET.get('category')
    edible_filter = request.GET.get('is_edible')

    if cat_filter:
        plants = plants.filter(category=cat_filter)
    
    if edible_filter:
        is_edible = True if edible_filter == 'true' else False
        plants = plants.filter(is_edible=is_edible)

    return render(request, "plant/all_plants.html", {"plants": plants})




def plant_detail(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant_id)[:3]

    return render(request, "plant/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants
    })



def plant_create(request: HttpRequest):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("plant:all_plants")
    else:
        form = PlantForm()
    return render(request, "plant/create_update.html", {"form": form, "title": "Add New Plant"})




def plant_update(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plant:plant_detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, "plant/create_update.html", {"form": form, "title": "Update Plant"})



def plant_delete(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    plant.delete()
    return redirect("plant:all_plants")




def plant_search(request: HttpRequest):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Plant.objects.filter(name__icontains=query)
    
    return render(request, "plant/search.html", {"results": results, "query": query})
