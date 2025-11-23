from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Plant, Comment, Category, Country
from .forms import PlantForm, CommentForm


# Create your views here.

def all_plants(request: HttpRequest):
    plants = Plant.objects.all()
    categories = Category.objects.all()
    countries = Country.objects.all() 
    cat_id = request.GET.get('category')
    edible_filter = request.GET.get('is_edible')
    country_id = request.GET.get('country')

    if cat_id:
        plants = plants.filter(category__id=cat_id)
    
    if edible_filter:
        is_edible = True if edible_filter == 'true' else False
        plants = plants.filter(is_edible=is_edible)
        
    if country_id:
        plants = plants.filter(native_countries__id=country_id)

    return render(request, "plant/all_plants.html", {
        "plants": plants,
        "categories": categories,
        "countries": countries 
    })




def plant_detail(request: HttpRequest, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    comments = plant.comments.all().order_by('-created_at')
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.plant = plant  
            new_comment.save()
            return redirect("plant:plant_detail", plant_id=plant.id)
    else:
        comment_form = CommentForm()
    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant_id)[:3]

    return render(request, "plant/plant_detail.html", {
        "plant": plant,
        "comments": comments,
        "comment_form": comment_form,
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
