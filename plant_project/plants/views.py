from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant
from .forms import PlantForm   
from django.db.models import Q


# صفحة عرض جميع النباتات + الفلترة
def all_plants(request):
    plants = Plant.objects.all().order_by("-id")# سويت ذا الامر هنا عشان يكون بصفحة ال ALL  يفلتر 

    category = request.GET.get("category")
    is_edible = request.GET.get("is_edible")

    if category:
        plants = plants.filter(category=category)

    if is_edible == "on":
        plants = plants.filter(is_edible=True)

    return render(request, 'plants/all_plants.html', {"plants": plants})


# صفحة التفاصيل
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    related = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    return render(request, 'plants/plant_detail.html', {
        "plant": plant,
        "related": related
    })


# صفحة إضافة النباتات والخ 
def add_plant(request):

    if request.method == "POST":
        name = request.POST.get("name")
        about = request.POST.get("about")
        used_for = request.POST.get("used_for")
        category = request.POST.get("category")
        is_edible = True if request.POST.get("is_edible") == "on" else False
        image = request.FILES.get("image")

        Plant.objects.create(
            name=name,
            about=about,
            used_for=used_for,
            category=category,
            is_edible=is_edible,
            image=image
        )

        return redirect("plants:all_plants")

    return render(request, "plants/add_plant.html")


# صفحة التحديث (ModelForm)
def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plants:plant_detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, 'plants/update_plant.html', {"form": form, "plant": plant})


# حذف النبات
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect("plants:all_plants")



def search(request):
    query = request.GET.get("q")  # الكلمة اللي كتبها المستخدم
    results = []

    if query:
        results = Plant.objects.filter(
            Q(name__icontains=query) |
            Q(about__icontains=query) |
            Q(used_for__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'plants/search.html', {
        "results": results,
        "query": query
    })
