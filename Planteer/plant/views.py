from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import Plant, Review, Country 
from django.db.models import Q
from .forms import PlantForm


# Create your views here.
def add_plant_view(request: HttpRequest):

   countries = Country.objects.all() # جلب جميع الدول من قاعدة البيانات
   plant_form = PlantForm()

   if request.method == "POST":
      plant_form = PlantForm(request.POST, request.FILES)
      if plant_form.is_valid():
         plant_form.save()
         return redirect('main:home_view')
      else:
         print("not valid form")

    #  new_plant = Plant(
        # name=request.POST["name"],
        # about=request.POST["about"],
        # image=request.FILES["image"],
        # used_for=request.POST["used_for"],
       #  category=request.POST["category"],
        # is_edible=request.POST["is_edible"]
     # )
      #new_plant.save()
      #new_plant.countries.set(request.POST.getlist("countries")) # ربط الدول بالنبات الجديد
     # return redirect('main:home_view')
   
   return render(request, 'plant/create.html', {"plant_form": plant_form, "countries": countries})  #"countries": countries# ارسال الدول للتمبلت


# Detail View
def plant_detail_view(request: HttpRequest, plant_id:int):

   plant = Plant.objects.get(pk=plant_id)
   reviews = Review.objects.filter(plant=plant)# هنا جبت الريفيوز
   related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]

   return render(request, 'plant/plant_detail.html', {"plant" : plant, "related_plants": related_plants, "reviews": reviews})# هنا بعت الريفيوز للتمبلت


# Update View
def plant_update_view(request: HttpRequest, plant_id:int):

   plant = Plant.objects.get(pk=plant_id)

   if request.method == "POST":
      plant.name = request.POST["name"]
      plant.about = request.POST["about"]
      if "image" in request.FILES:
        plant.image = request.FILES["image"]
      plant.used_for = request.POST["used_for"]
      plant.category = request.POST["category"]
      plant.is_edible = request.POST["is_edible"]
      plant.save()
      return redirect('plant:plant_detail_view', plant_id=plant.id)
   
   return render(request, "plant/plant_update.html", {"plant": plant})

# Delete View
def plant_delete_view(request: HttpRequest, plant_id:int):

   plant = Plant.objects.get(pk=plant_id)
   plant.delete()

   return redirect('main:home_view')
  
# All Plants View
def all_plant_view(request: HttpRequest):

   plant = Plant.objects.all()

   return render(request, 'plant/all_plant.html', {"plant": plant})

# Search Plants View
def search_plant_view(request:HttpRequest):

   query = request.GET.get("search", "")
   plant = Plant.objects.filter(
      Q(name__icontains=query) |
      Q(category__icontains=query) |
      Q(used_for__icontains=query) |
      Q(about__icontains=query)
   )
   return render(request, "plant/search_plant.html", {"plant": plant,"search_query": query})


def add_review_view(request:HttpRequest, plant_id):
   
   if request.method == "POST":
      plant_object = Plant.objects.get(pk=plant_id)
      new_review=Review(plant=plant_object,
      name=request.POST["name"],
      comment=request.POST["comment"],)
   new_review.save()
   
   return redirect("plant:plant_detail_view", plant_id=plant_id )