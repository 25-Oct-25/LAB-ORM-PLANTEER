from django.shortcuts import render ,redirect
from .models import Plant

from .forms import PlantForm



# Create your views here.
def plants_add_view(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:home_view')
    else:
        form = PlantForm()

    return render(request, 'plants/add_plant.html')



def plants_detail_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant_id)[:3]

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'related_plants': related_plants
    })

def plants_update_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)

        if form.is_valid():

            plant.name = request.POST.get("name")
            plant.about = request.POST.get("about")
            plant.used_for = request.POST.get("used_for")
            plant.category = request.POST.get("category")
            plant.is_edible = "is_edible" in request.POST

            if "image" in request.FILES:
                plant.image = request.FILES["image"]

            plant.save()

            return redirect("plants:plants_detail_view", plant_id=plant_id)

    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/plants_update.html", {
        "plant": plant,
        "form": form,
    })




def plants_delet_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    plant.delete()
    return redirect('main:home_view')


def plants_search_view(request):
    query = request.GET.get("search")
    plants = []

    if query:
        plants = Plant.objects.filter(name__icontains=query)

    return render(request, "plants/plants_search.html", {'plants': plants, 'query': query}) 

def plants_list_view(request):
    plants = Plant.objects.all()
    count = plants.count()
    return render(request, 'plants/plants_list.html', {'plants': plants, 'count': count})
