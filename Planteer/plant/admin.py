from django.contrib import admin
from .models import Plant, Review ,Contact


# Register your models here.

class PlantAdmin(admin.ModelAdmin):
    list_display=("name","is_edible","category")
    list_filter =("category",)

class ContactAdmin(admin.ModelAdmin):
    list_display=("first_name","message","email")    


class ReviewAdmin(admin.ModelAdmin):
    list_display=("plant","comment")   

admin.site.register(Plant,PlantAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Review,ReviewAdmin)



