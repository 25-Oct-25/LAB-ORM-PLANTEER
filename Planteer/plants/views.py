from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant
from .forms import PlantForm

def all_plants(request):
    plants = Plant.objects.all()
    
    category_filter = request.GET.get('category')
    edible_filter = request.GET.get('is_edible')

    if category_filter:
        plants = plants.filter(category=category_filter)
    
    if edible_filter:
        is_edible = edible_filter.lower() == 'true'
        plants = plants.filter(is_edible=is_edible)

    return render(request, 'plants/all_plants.html', {'plants': plants})

def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    
    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant_id)[:3]
    
    return render(request, 'plants/plant_detail.html', {
        'plant': plant, 
        'related_plants': related_plants
    })

def new_plant(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('all_plants')
    else:
        form = PlantForm()
    return render(request, 'plants/new_plant.html', {'form': form})

def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/update_plant.html', {'form': form, 'plant': plant})

def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    plant.delete()
    return redirect('all_plants')

def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    
    # If user clicked "Yes, Delete" button (POST request)
    if request.method == "POST":
        plant.delete()
        return redirect('all_plants')
        
    # If user just clicked the "Delete" link (GET request), show confirmation page
    return render(request, 'plants/delete_plant.html', {'plant': plant})

def search_plants(request):
    query = request.GET.get('q')
    plants = []
    if query:
        plants = Plant.objects.filter(name__icontains=query)
    return render(request, 'plants/search.html', {'plants': plants, 'query': query})