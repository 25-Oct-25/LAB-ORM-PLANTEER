from django.contrib import admin
from .models import Plant, Review ,Contact, Country


# Register your models here.

class PlantAdmin(admin.ModelAdmin):
    list_display=("name","is_edible")


class ContactAdmin(admin.ModelAdmin):
    list_display=("first_name","message","email")    


class ReviewAdmin(admin.ModelAdmin):
    list_display=("plant","comment") 

class CountryAdmin(admin.ModelAdmin):
    list_display=("name",)      

admin.site.register(Plant,PlantAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Country,CountryAdmin)



