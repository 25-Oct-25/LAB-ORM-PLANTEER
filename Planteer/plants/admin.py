from django.contrib import admin
from .models import Plant, Country # 1. استيراد موديل Country

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'category', 'display_countries') 
    
    list_filter = ('category', 'is_edible', 'countries') 
    
    search_fields = ('name', 'about')

    def display_countries(self, obj):
        return ", ".join([country.name for country in obj.countries.all()])
    display_countries.short_description = 'Native Countries'