from django.contrib import admin
from .models import Plant, Comment


class CommentInline(admin.TabularInline):
    """تعليقات تظهر داخل صفحة النبتة في لوحة التحكم"""
    model = Comment
    extra = 1                 
    fields = ("name", "content", "date_added")
    readonly_fields = ("date_added",) 


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    """كيف تبغى شكل جدول النباتات في لوحة التحكم"""
    list_display = ("name", "category", "is_edible", "created_at")
    list_filter = ("category", "is_edible")
    search_fields = ("name", "about", "used_for")
    ordering = ("-created_at",)
    inlines = [CommentInline] 


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """جدول خاص بالتعليقات في لوحة التحكم"""
    list_display = ("name", "plant", "date_added")
    search_fields = ("name", "content", "plant__name")
    list_filter = ("date_added",)
    ordering = ("-date_added",)
