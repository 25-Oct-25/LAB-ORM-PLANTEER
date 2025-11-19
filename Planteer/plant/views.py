from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from . models import Plant

# Create your views here.


def all_plants_view(request: HttpRequest):


    if "category" in request.GET and request.GET["category"] == "all" :
        plants = Plant.objects.all()
        
    elif "category" in request.GET and request.GET["category"] == "fruits" :
        plants = Plant.objects.filter(category = "fruits")
        
    elif "category" in request.GET and request.GET["category"] == "vegetables" :
        plants = Plant.objects.filter(category = "vegetables")
        
    else :
        plants = Plant.objects.filter(category = "flowers")
    
        
    if "is_edible" in request.GET :
        plants = plants.filter(is_edible = request.GET["is_edible"] == "true")
        
   
    return render(request, "plant/all_plants.html" , { "plants": plants})

def create_plant_view(request: HttpRequest):
    # هنا اعبي كل البيانات الي موجوده بالمودل 
    if request.method == "POST":
        new_plant = Plant(
            name=request.POST["name"],
            about=request.POST["about"],
            used_for=request.POST["used_for"],
            category=request.POST["category"],
            is_edible=request.POST.get("is_edible") == "on",
            created_at=datetime.now(),
            image=request.FILES["image"]
        )
        new_plant.save() # هنا احفظهم بقاعده البيانات 
        return redirect('main:home_view')  # بعد الاضافه يوديه صفحه الهوم 

    return render(request, "plant/create_plant.html",  {"CategoryChoices" : Plant.CategoryChoices.choices})


def plant_detail_view(request: HttpRequest , plant_id: int ): # هنا اعين باث باراميتر عشان اقدر اعرض و اوصل للبيانات 
    plant = Plant.objects.get(pk=plant_id)

    plants = Plant.objects.filter(category=plant.category).exclude(pk=plant.id)
    

    return render(request, "plant/plant_detail.html", {"plant" : plant , "plants" : plants })


    
def plant_update_view(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(pk=plant_id)

    if request.method == "POST": #هنا نفس الي طبقنا في الانشاء بس نتاكد اول اذا ادخال مو عرض 
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.category = request.POST["category"]
        plant.is_edible = request.POST.get("is_edible") == "on"
        plant.created_at = datetime.now()  

        if "image" in request.FILES: # اول شي اشيك اذا اليوزر دخل صوره حدث , احدث الصوره 
            plant.image = request.FILES["image"]

        plant.save()
        return redirect('plant:plant_detail_view', plant_id=plant.id) # هنا بعد ما عدلها ارجعه لصفحه الديتيل و الثانيه لان الباث ياخذ قيمه فلازم اسندها له 

    return render(request, "plant/update_plant.html", {"plant": plant})


def plant_delete_view(request: HttpRequest , plant_id: int):

    plant = Plant.objects.get(pk=plant_id)

    plant.delete()
    return redirect('main:home_view')


def plant_search_view(request:HttpRequest):
    print(request.GET)
    if "search" in request.GET and len(request.GET["search"]) >= 3 :
        plants = Plant.objects.filter(name__contains=request.GET["search"])
    else:
        plants = []
        
    return render(request, "plant/plant_search.html" , {"plants" : plants})