from django.contrib import admin
from .models import Plant, Review, Country

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_edible', 'created_at']
    list_filter = ['category', 'is_edible']
    search_fields = ['name', 'description']
    filter_horizontal = ('countries',)  # هذا يتيح اختيار أكثر من دولة بسهولة

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['plant', 'name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['name', 'comment']

admin.site.register(Country)
