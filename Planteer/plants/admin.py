from django.contrib import admin
from .models import Plant,Comment,Country

class PlantAdmin(admin.ModelAdmin):
    list_display= ("name", "category")
    list_filter=("category",)


class CommentAdmin(admin.ModelAdmin):
    list_display= ("name",)
   

admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Country)
