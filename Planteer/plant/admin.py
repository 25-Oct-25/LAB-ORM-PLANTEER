from django.contrib import admin
from .models import Plant, Comment, Category, Country

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'flag']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_edible', 'created_at']
    list_filter = ['category', 'is_edible']
    search_fields = ['name', 'about']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'plant', 'created_at']
    list_filter = ['created_at']