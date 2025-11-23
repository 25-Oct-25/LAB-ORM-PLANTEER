from django.shortcuts import render, redirect
from .models import Plant, Comment, Country

def plants_all_view(request):

    category = request.GET.get("category")
    edible = request.GET.get("edible")
    country = request.GET.get("country")

    plants = Plant.objects.all()
    countries = Country.objects.all()

    if category and category != "all":
        plants = plants.filter(category=category)

  
    if edible == "yes":
        plants = plants.filter(is_edible=True)
    elif edible == "no":
        plants = plants.filter(is_edible=False)

    if country and country != "all":
        plants = plants.filter(Countries__id=country)

    return render(request, "plants/plants_all.html", {
        "plants": plants,
        "selected_category": category,
        "selected_edible": edible,
        "countries": countries,
        "selected_country": country,
    })

def plants_new_view(request):
    countries = Country.objects.all()  

    if request.method == "POST":
        name = request.POST.get("name")
        about = request.POST.get("about")
        used_for = request.POST.get("used_for")
        is_edible = bool(request.POST.get("is_edible"))
        image = request.FILES.get("image")

        plant = Plant.objects.create(
            name=name,
            about=about,
            used_for=used_for,
            is_edible=is_edible,
            image=image,
        )

        selected_countries = request.POST.getlist("countries")
        plant.Countries.set(selected_countries)


        return redirect("plants:plants_all")

    return render(request, "plants/plants_new.html", {"countries": countries})



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
    countries = Country.objects.all()

    if request.method == "POST":
        plant.name = request.POST.get("name")
        plant.about = request.POST.get("about")
        plant.used_for = request.POST.get("used_for")
        plant.category = request.POST.get("category")
        plant.is_edible = bool(request.POST.get("is_edible"))

        if request.FILES.get("image"):
            plant.image = request.FILES.get("image")

        selected_countries = request.POST.getlist("countries")
        plant.Countries.set(selected_countries)


        plant.save()
        return redirect("plants:plants_detail", plant_id=plant_id)

    return render(request, "plants/plants_update.html", {"plant": plant, "countries": countries})

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

def add_comment_view(request,plant_id):

    if request.method == "POST":
        plant_object=Plant.objects.get(pk=plant_id)
        new_comment=Comment(plant=plant_object,name=request.POST["name"], content=request.POST["content"])
        new_comment.save()
        return redirect("plants:plants_detail", plant_id=plant_id)  
    
def country_plants_view(request, country_id):
    country = Country.objects.get(id=country_id)
    plants = Plant.objects.filter(Countries=country)

    return render(request, "plants/country_plants.html", {
        "country": country,
        "plants": plants
    })
