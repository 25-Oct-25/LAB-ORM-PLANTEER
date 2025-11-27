from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Plant, Comment, Country 
from .forms import PlantForm, CommentForm
from django.contrib.auth.decorators import login_required


def plant_list(request):
    plants = Plant.objects.all()

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')
    country_id = request.GET.get('country')

    if category and category != 'all':
        plants = plants.filter(category=category)
    if is_edible == 'true':
        plants = plants.filter(is_edible=True)
        
    if country_id:
        plants = plants.filter(countries__id=country_id) 
        
    context = {
        'plants': plants,
        'categories': Plant.CATEGORY_CHOICES, 
        'countries': Country.objects.all(),
        'selected_category': category,
        'selected_is_edible': is_edible,
        'selected_country_id': country_id,
    }
    return render(request, 'plants/plant_list.html', context)


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"/login/?next=/plants/{plant_id}/")

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.plant = plant
            new_comment.name = request.user.username  # ✨ اسم اليوزر
            new_comment.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        comment_form = CommentForm()

    comments = plant.comments.all()

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:4]

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments,
        'comment_form': comment_form,
    })



@login_required
def plant_create(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_list')
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {
        'form': form,
        'title': 'Add New Plant',
    })


@login_required
def plant_update(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/plant_form.html', {
        'form': form,
        'title': 'Update Plant',
    })


@login_required
def plant_delete(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        plant.delete()
        return redirect('plants:plant_list')
    return render(request, 'plants/plant_confirm_delete.html', {
        'plant': plant
    })


def plant_search_view(request):
    plants_qs = Plant.objects.all()

    query = request.GET.get("q", "").strip()
    
    if query:
        plants_qs = plants_qs.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'results': plants_qs, 
        'query': query,
    }
    
    return render(request, 'plants/plant_search.html', context)


def country_detail(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    plants = country.native_plants.all().order_by('name') 

    context = {
        'country': country,
        'plants': plants,
    }
    return render(request, 'plants/country_detail.html', context)

@login_required
def plant_update(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.user != plant.owner and not request.user.is_superuser:
        return redirect('plants:plant_detail', plant_id=plant.id)

    ...

@login_required
def plant_delete(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.user != plant.owner and not request.user.is_superuser:
        return redirect('plants:plant_detail', plant_id=plant.id)

    ...
