from django.contrib import admin
from .models import Plant, Country, Review

# Register your models here.




class PlantAdmin(admin.ModelAdmin): # يعرض البيانات في لوحة الادمن 
    list_display = ["name", "category", "is_edible", "created_at"]# يعرض البيانات في لوحة الادمن بشكل اعمده
    list_filter = () # فلتره البيانات في لوحة الادمن
    search_fields = () # اضافه شريط بحث في لوحة الادمن


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["name", "plant", "created_at"]
    list_filter = ["created_at"]

admin.site.register(Plant, PlantAdmin)
admin.site.register(Country)
admin.site.register(Review, ReviewAdmin)