from django.contrib import admin
from .models import Plant, Comment, Country

# Register your models here.

class PlantAdmin (admin.ModelAdmin):
    list_display = ("name", "category", "created_at")
    list_filter = ("category", "created_at")




class CommentAdmin (admin.ModelAdmin):
    list_display = ("full_name", "created_at")
    list_filter = ("full_name", "plant", "created_at")


admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country)