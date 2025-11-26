from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from plants.models import Plant
from .models import Country
from .forms import CountryForm

# Create your views here.
def add_country_view(request: HttpRequest):
    if request.method == "POST":
        country_form = CountryForm(request.POST, request.FILES)
        if country_form.is_valid():
            country_form.save()
            return redirect("countries:countries_view")
    else:
        country_form = CountryForm()

    return render(request, "countries/add_country.html", {"country_form": country_form})

#for all countries
def countries_view(request : HttpRequest):
    
    countries = Country.objects.all()
    
    return render(request, "countries/countries.html", {"countries" : countries})


#for one country based on id
def country_view(request : HttpRequest, country_id):
    country = Country.objects.get(id = country_id)
    
    plant_by_country = Plant.objects.filter(country = country)

    plants = country.plant_set.all()
    print(plant_by_country)
    print(plants)
    
    return render(request, "countries/country.html", {"country" : country})