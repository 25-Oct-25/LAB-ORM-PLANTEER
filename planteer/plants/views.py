from django.shortcuts import render, get_object_or_404, redirect
from .models import Plant,Comment,Country
from .forms import PlantForm, CommentForm
from django.contrib.auth.decorators import user_passes_test

def staff_required(login_url='/accounts/login/'):
    return user_passes_test(lambda u: u.is_active and u.is_staff, login_url=login_url)

def plant_list_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    selected_countries = request.GET.getlist('country') 

    plants = Plant.objects.all().prefetch_related('countries')

    if query:
        plants = plants.filter(name__icontains=query)

    if category and category != 'ALL':
        plants = plants.filter(category=category)

    if is_edible == 'true':
        plants = plants.filter(is_edible=True)
    elif is_edible == 'false':
        plants = plants.filter(is_edible=False)

    if selected_countries:
        plants = plants.filter(countries__id__in=selected_countries)

    context = {
        'plants': plants.distinct(),              
        'countries': Country.objects.all(),
        'selected_countries': selected_countries, 
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

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.plant = plant
            comment.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        comment_form = CommentForm()

    context = {
        'plant': plant,
        'related_plants': related_plants,
        'comment_form': comment_form,
    }

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
        'comment_form':comment_form
    })

@staff_required(login_url='/accounts/login/')
def plant_create_view(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_list')
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Add Plant'})

@staff_required(login_url='/accounts/login/')
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

@staff_required(login_url='/accounts/login/')
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

def country_detail_view(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    plants = country.plants.all().prefetch_related('countries')
    return render(request, 'plants/country_detail.html', {'country': country, 'plants': plants})
