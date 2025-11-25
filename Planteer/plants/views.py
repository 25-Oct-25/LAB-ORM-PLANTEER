from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Plant, Country,Comment, Country
from .forms import PlantForm, CommentForm
from django.core.paginator import Paginator

from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# 1) Show all plants
def plants_view(request: HttpRequest):
    plants = Plant.objects.all().order_by('-created_at')
    return render(request, 'plants/all_plants.html', {"plants": plants})

# 2) Plant details
# def plant_details_view(request, plant_id):
#     plant = get_object_or_404(Plant, id=plant_id)
#     related = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]
#     comments = plant.comments.all()

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.plant = plant
#             new_comment.save()
#             return redirect('plants:plant_details_view', plant_id=plant.id)
#     else:
#         form = CommentForm()

#     context = {
#         'plant': plant,
#         'related': related,
#         'comments': comments,
#         'form': form,
#     }
#     return render(request, 'plants/plant_detail.html', context)


def plant_details_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    related = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:6]
    comments = plant.comments.order_by('-date_added')
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to add a comment.")
            # redirect to login with next back to this page
            login_url = f"{reverse('accounts:login')}?next={request.path}"
            return redirect(login_url)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.name = request.user.get_full_name() or request.user.username
            comment.plant = plant
            comment.save()
            messages.success(request, "Comment added.")
            return redirect('plants:plant_details_view', plant_id=plant.id)
    else:
        form = CommentForm()

    context = {"plant": plant, "related": related, "comments": comments, "form": form}
    return render(request, "plants/plant_detail.html", context)


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

# 7) Filtering by country
def plants_by_country(request, country_id):
    country = Country.objects.get(id=country_id)
    plants = country.plants.all()
    return render(request, 'plants/plants_by_country.html', {
        'country': country,
        'plants': plants
    })


# 8) Filter & Pagination
def plants_view(request):
    plants = Plant.objects.all().order_by('-created_at')

    # Filtering
    category = request.GET.get('category')
    country_id = request.GET.get('country')
    
    if category:
        plants = plants.filter(category=category)
    if country_id:
        plants = plants.filter(countries__id=country_id)

    # Pagination
    paginator = Paginator(plants, 6)  # 6 plants per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get list of all categories and countries for filter dropdowns
    categories = Plant.Category.choices
    countries = Country.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'countries': countries,
        'selected_category': category,
        'selected_country': country_id,
    }
    return render(request, 'plants/all_plants.html', context)
