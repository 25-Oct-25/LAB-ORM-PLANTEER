from django.shortcuts import render , redirect
from django.http import HttpRequest
from .models import Plant ,Contact
from .forms import PlantForm, ContactForm
# Create your views here.

def all_plants_view(request:HttpRequest):
    is_edible= request.GET.get("is_edible")
    category= request.GET.get("category")
    plants=Plant.objects.all()
    if is_edible:
        plants=Plant.objects.all().filter(is_edible=is_edible)
    
    if category:
        plants=Plant.objects.all().filter(category=category)

    return render(request,"plant/plants.html",{"plants":plants})

def add_plant_view(request:HttpRequest):
    if request.method=="POST":
        plant_form=PlantForm(request.POST , request.FILES)
        if plant_form.is_valid():
            plant_form.save()
            return redirect('main:home_view')
        else:
            print("not valid form")

    return render(request,"plant/add.html", {"CategoryChoices":Plant.CategoryChoices.choices})

def plant_detail_view(request:HttpRequest, plant_id:int):
    plant=Plant.objects.get(pk=plant_id)
    related_plants=Plant.objects.all().filter(category=plant.category).exclude(pk=plant_id)[0:3]
    return render(request,"plant/details.html", {"plant":plant ,"related_plants":related_plants})


def plant_update_view(request:HttpRequest, plant_id:int):
    plant=Plant.objects.get(pk=plant_id)
    if request.method =="POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.is_edible = request.POST["is_edible"]
        plant.category=request.POST["category"]
        if "image" in request.FILES: plant.image = request.FILES["image"]
        plant.save()
        return redirect("plant:plant_detail_view", plant_id=plant.id)
    return render(request,"plant/update.html", {"plant":plant})

def plant_delete_view(request:HttpRequest, plant_id:int):
    plant=Plant.objects.get(pk=plant_id)
    plant.delete()

    return redirect("main:home_view")

def send_message_view(request:HttpRequest):
    if request.method=="POST":
        contact_form=ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('main:home_view')
        else:
            print("not valid form")

    return render(request,"plant/contact.html")   

def all_messages_view(request:HttpRequest):
    messages=Contact.objects.all()
    return render(request,"plant/messages.html",{"msg":messages})

def search_plants_view(request:HttpRequest):
    
    if "search" in request.GET and len(request.GET["search"])>= 3:
        plants=Plant.objects.filter(name__contains=request.GET["search"])
    else:
        plants=[]

    return render(request, "plant/search.html" ,{"plants":plants})