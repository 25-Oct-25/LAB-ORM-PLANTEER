from django.shortcuts import render, redirect
from .models import Plant

def plants_all_view(request):

    category = request.GET.get("category")
    edible = request.GET.get("edible")

    plants = Plant.objects.all()

   
    if category and category != "all":
        plants = plants.filter(category=category)

  
    if edible == "yes":
        plants = plants.filter(is_edible=True)
    elif edible == "no":
        plants = plants.filter(is_edible=False)

    return render(request, "plants/plants_all.html", {
        "plants": plants,
        "selected_category": category,
        "selected_edible": edible
    })


def plants_new_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        about = request.POST.get("about")
        used_for = request.POST.get("used_for")
        category = request.POST.get("category")
        is_edible = bool(request.POST.get("is_edible"))
        image = request.FILES.get("image")

        Plant.objects.create(
            name=name,
            about=about,
            used_for=used_for,
            category=category,
            is_edible=is_edible,
            image=image,
        )

        return redirect("plants:plants_all")

    return render(request, "plants/plants_new.html")

def plants_detail_view(request, plant_id):
    try:
        plant = Plant.objects.get(id=plant_id)
    except Plant.DoesNotExist:
        return redirect("plants:plants_all")

    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]

    return render(request, "plants/plants_detail.html", {
        "plant": plant,
        "related_plants": related_plants
    })


def plants_update_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        plant.name = request.POST.get("name")
        plant.about = request.POST.get("about")
        plant.used_for = request.POST.get("used_for")
        plant.category = request.POST.get("category")
        plant.is_edible = bool(request.POST.get("is_edible"))

        if request.FILES.get("image"):
            plant.image = request.FILES.get("image")

        plant.save()
        return redirect("plants:plants_detail", plant_id=plant_id)

    return render(request, "plants/plants_update.html", {"plant": plant})

def plants_delete_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    plant.delete()
    return redirect('plants:plants_all')



def plants_search_view(request):
    query = request.GET.get("q")  
    results = []

    if query:
        results = Plant.objects.filter(name__icontains=query)

    return render(request, "plants/plants_search.html", {
        "query": query,
        "results": results,
        "count": results.count(),
    })
   
