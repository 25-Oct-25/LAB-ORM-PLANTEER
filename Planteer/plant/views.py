from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from . models import Plant, Comment, Country


# Create your views here.

def all_plants_view(request: HttpRequest):

    plants = Plant.objects.all()

    # Filter by category
    category = request.GET.get("category")
    if category and category != "all":
        plants = plants.filter(category=category)

    # Filter by edible
    is_edible = request.GET.get("is_edible")
    if is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif is_edible == "false":
        plants = plants.filter(is_edible=False)

    # Filter by country
    country_filter = request.GET.get("country")
    if country_filter and country_filter != "ALL":
        plants = plants.filter(countries__id=country_filter)

    plants = plants.distinct()

    count = plants.count()
    countries = Country.objects.all()
    categories = Plant.CategoryChoices.choices

    return render(request, "plant/all_plants.html", {
        "plants": plants,
        "count": count,
        "countries": countries,
        "categories": categories,
    })


def create_plant_view(request: HttpRequest):
    # هنا اعبي كل البيانات الي موجوده بالمودل 
    countries = Country.objects.all()   #  لازم نجيب الدول عشان نعرضها في صفحة الانشاء

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
        new_plant.save()  # هنا احفظهم بقاعده البيانات 

        #  بعد الحفظ — نحفظ الدول (ManyToMany)
        selected_countries = request.POST.getlist("countries")  # يرجع لستة IDs
        new_plant.countries.set(selected_countries)

        return redirect('main:home_view')  # بعد الاضافه يوديه صفحه الهوم 

    return render(
        request, 
        "plant/create_plant.html",  
        {
            "CategoryChoices" : Plant.CategoryChoices.choices,  # هنا لازم امرر ال choices
            "countries": countries  #  تمرير قائمة الدول الى صفحة الانشاء
        }
    )

def plant_detail_view(request: HttpRequest , plant_id: int ): # هنا اعين باث باراميتر عشان اقدر اعرض و اوصل للبيانات 
    plant = Plant.objects.get(pk=plant_id)

    plants = Plant.objects.filter(category=plant.category).exclude(pk=plant.id)
    Comments = Comment.objects.filter(plant=plant)

    return render(request, "plant/plant_detail.html", {"plant" : plant , "plants" : plants, "comments" : Comments })



def plant_comment_view(request: HttpRequest , plant_id: int ):
    plant = Plant.objects.get(pk=plant_id)

    if request.method == "POST":

        new_comment = Comment(
                plant = plant, #plant from db = plant object 
                full_name=request.POST["full_name"],
                content=request.POST["content"],
        )    
        new_comment.save()
        return redirect("plant:plant_detail_view" , plant_id = plant_id)

    
def plant_update_view(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(pk=plant_id)
    countries = Country.objects.all()   #  لازم نرسل الدول عشان نعرض الـ checkbox في الفورم

    if request.method == "POST":  # هنا نفس الي طبقنا في الانشاء بس نتاكد اول اذا ادخال مو عرض 
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.category = request.POST["category"]
        plant.is_edible = request.POST.get("is_edible") == "on"
        plant.created_at = datetime.now()  

        #  تحديث الدول المختارة (ManyToMany)
        # getlist يرجع قائمة IDs لأن المستخدم يقدر يختار أكثر من دولة
        selected_countries = request.POST.getlist("countries")
        plant.countries.set(selected_countries)  #  هذا يحفظ الدول الجديدة بدون حذف الكود القديم

        if "image" in request.FILES:  # اول شي اشيك اذا اليوزر دخل صوره حدث , احدث الصوره 
            plant.image = request.FILES["image"]

        plant.save()
        return redirect(
            'plant:plant_detail_view', 
            plant_id=plant.id
        )  # هنا بعد ما عدلها ارجعه لصفحه الديتيل و الخانه الثانيه لان الباث ياخذ قيمه فلازم اسندها له 

    return render(
        request, 
        "plant/update_plant.html", 
        {
            "plant": plant,
            "countries": countries  #  علشان نظهر الدول في صفحة التعديل
        }
    )


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


def plants_country_view(request, country_id):
    country = Country.objects.get(id=country_id)
    plants = Plant.objects.filter(countries=country)  
    count = plants.count()

    return render(request, 'plant/plant_country.html', {
        'country': country,
        'plants': plants,
        'count': count
    })