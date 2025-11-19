from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Plant
from .forms import PlantForm, PlantSearchForm


from django.db.models import Q

def plant_list(request):
   
  
    plants = Plant.objects.all().order_by("-created_at")

    
    form = PlantSearchForm(request.GET or None)

    if form.is_valid():
        
        search = form.cleaned_data.get("search", "").strip()
        category = form.cleaned_data.get("category") or ""
        is_edible = form.cleaned_data.get("is_edible") or ""

        
        if search:
            plants = plants.filter(
                Q(name__icontains=search) |
                Q(about__icontains=search) |
                Q(used_for__icontains=search)
            )

       
        if category:
            plants = plants.filter(category=category)

       
        if is_edible == "true":
            plants = plants.filter(is_edible=True)
        elif is_edible == "false":
            plants = plants.filter(is_edible=False)

    return render(request, "plants/plant_list.html", {
        "plants": plants,
        "form": form,
    })


def plant_delete(request, plant_id):
    
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect("plants:all")  # اسم المسار في urls.py

    return render(request, "plants/plant_confirm_delete.html", {
        "plant": plant,
    })


def plant_create(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("plants:all")
    else:
        form = PlantForm()
    return render(request, "plants/plant_form.html",
                  {"form": form, "title": "Add Plant"})


def plant_update(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/plant_form.html",
                  {"form": form, "title": "Update Plant"})


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    related_plants = (
        Plant.objects.filter(category=plant.category)
        .exclude(id=plant.id)[:4]
    )

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
    })



def plant_search(request):
    form = PlantSearchForm(request.GET or None)
    plants = Plant.objects.none()

    if form.is_valid():
        q = form.cleaned_data.get("q") or ""
        category = form.cleaned_data.get("category") or ""
        is_edible = form.cleaned_data.get("is_edible") or ""

        plants = Plant.objects.all()

        if q:
            plants = plants.filter(
                Q(name__icontains=q) |
                Q(about__icontains=q) |
                Q(used_for__icontains=q)
            )

        if category:
            plants = plants.filter(category=category)

        if is_edible == "true":
            plants = plants.filter(is_edible=True)
        elif is_edible == "false":
            plants = plants.filter(is_edible=False)

    return render(request, "plants/plant_search.html", {
        "form": form,
        "plants": plants,
    })
