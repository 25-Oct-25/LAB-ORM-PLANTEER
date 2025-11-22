from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Plant , Comment
from .forms import PlantForm, PlantSearchForm, CommentForm


from django.db.models import Q
def plant_list(request):
   
    search    = request.GET.get("search", "").strip()
    category  = request.GET.get("category", "")
    is_edible = request.GET.get("is_edible", "")

   
    plants = Plant.objects.all().order_by("-created_at")

   
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

    
    form = PlantSearchForm(initial={
        "search": search,
        "category": category,
        "is_edible": is_edible,
    })

    return render(request, "plants/plant_list.html", {
        "plants": plants,
        "form": form,
    })

def plant_search(request):
    
    search    = request.GET.get("search", "").strip()
    category  = request.GET.get("category", "")
    is_edible = request.GET.get("is_edible", "")

    
    plants = Plant.objects.all().order_by("-created_at")

  
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

  
    form = PlantSearchForm(initial={
        "search": search,
        "category": category,
        "is_edible": is_edible,
    })

    return render(request, "plants/plant_search.html", {
        "plants": plants,
        "form": form,
    })


def plant_delete(request, plant_id):
    
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect("plants:all") 

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

   
    comments = plant.comments.all()


    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False) 
            new_comment.plant = plant             
            new_comment.save()                    
            return redirect("plants:detail", plant_id=plant.id)
    else:
       
        form = CommentForm()

  
    related_plants = (
        Plant.objects.filter(category=plant.category)
        .exclude(id=plant.id)[:4]
    )

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments,
        "comment_form": form,
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
