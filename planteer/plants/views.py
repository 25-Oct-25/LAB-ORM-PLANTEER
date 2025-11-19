from django.shortcuts import render, get_object_or_404, redirect
from .models import Plant
from .forms import PlantForm

def plant_list_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    plants = Plant.objects.all()

    if query:
        plants = plants.filter(name__icontains=query)

    if category and category != 'ALL':
        plants = plants.filter(category=category)

    if is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif is_edible == 'false':
        plants = plants.filter(is_edible=False)

    context = {
        'plants': plants,
        'categories': Plant.Category.choices,
        'selected_category': category or 'ALL',
        'selected_is_edible': is_edible or '',
        'query': query,   
    }
    return render(request, 'plants/plant_list.html', context)


def plant_detail_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
    })


def plant_create_view(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_list')
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Add Plant'})


def plant_update_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Update Plant'})


def plant_delete_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        plant.delete()
        return redirect('plants:plant_list')
    return render(request, 'plants/plant_delete.html', {'plant': plant})


def plant_search_view(request):
    query = request.GET.get('q', '')
    results = Plant.objects.all()
    if query:
        results = results.filter(name__icontains=query)
    return render(request, 'plants/plant_search.html', {
        'query': query,
        'results': results,
    })
