from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from .models import Plant, Comment, Country
from .forms import PlantForm, CommentForm


# ALL PLANTS PAGE (List + Filters + Add Comment)
def all_plants(request):

    plants = Plant.objects.all().order_by("-id")

    # Filters
    category = request.GET.get("category")
    is_edible = request.GET.get("is_edible")
    country_id = request.GET.get("country")

    if category:
        plants = plants.filter(category=category)

    if is_edible == "on":
        plants = plants.filter(is_edible=True)

    if country_id:
        plants = plants.filter(countries__id=country_id)

    # Add Comment
    if request.method == "POST":

        #  منع غير المسجلين
        if not request.user.is_authenticated:
            return redirect("account:signin")

        plant_id = request.POST.get("plant_id")
        plant = get_object_or_404(Plant, id=plant_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.plant = plant

            # ⭐ ربط التعليق بالمستخدم الحقيقي
            comment.user = request.user  

            comment.save()

        return redirect("plants:all_plants")

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "countries": Country.objects.all(),
    })



# DETAILS PAGE
def plant_detail(request, plant_id):

    plant = get_object_or_404(
        Plant.objects.annotate(
            comments_count=Count('comments')
        ),
        id=plant_id
    )

    related = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related": related,
        "comments_count": plant.comments_count
    })



# ADD PLANT PAGE
def add_plant(request):

    if request.method == "POST":

        name = request.POST.get("name")
        about = request.POST.get("about")
        used_for = request.POST.get("used_for")
        category = request.POST.get("category")
        is_edible = True if request.POST.get("is_edible") == "on" else False
        image = request.FILES.get("image")

        plant = Plant.objects.create(
            name=name,
            about=about,
            used_for=used_for,
            category=category,
            is_edible=is_edible,
            image=image
        )

        country_ids = request.POST.getlist("countries")
        plant.countries.set(country_ids)

        return redirect("plants:all_plants")

    return render(request, "plants/add_plant.html", {
        "countries": Country.objects.all()
    })



# UPDATE PLANT PAGE
def update_plant(request, plant_id):

    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plants:plant_detail", plant_id=plant.id)

    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/update_plant.html", {
        "form": form,
        "plant": plant
    })



# DELETE PLANT
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect("plants:all_plants")



# SEARCH PAGE
def search(request):

    query = request.GET.get("q")
    results = []

    if query:
        results = Plant.objects.filter(
            Q(name__icontains=query) |
            Q(about__icontains=query) |
            Q(used_for__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, "plants/search.html", {
        "results": results,
        "query": query
    })
