from django.contrib import admin
from .models import Plant, Comment, Country

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display=('name','plant','created_at')
    list_filter=('created_at','plant')
    search_fields=('name','content','plant__name')

admin.site.register(Comment, CommentAdmin)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Country,CountryAdmin)

class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_edible')
    list_filter = ('category', 'is_edible', 'countries')
    search_fields = ('name', 'about', 'used_for')
    filter_horizontal = ('countries',)  
admin.site.register(Plant,PlantAdmin)

