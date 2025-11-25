from django.contrib import admin
from .models import Plant, Comment, Country



# Country Admin

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)



#Plant Admin

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "is_edible", "created_at")
    list_filter = ("category", "is_edible", "created_at", "countries")
    search_fields = ("name", "about", "used_for")
    ordering = ("-created_at",)

    #  عرض الدول داخل صفحة النبات
    filter_horizontal = ("countries",)

#Comment Admin 

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plant", "created_at")  # ← عدلنا username إلى user
    list_filter = ("created_at", "plant")
    search_fields = ("text", "user__username")            # ← البحث باسم المستخدم الحقيقي
    ordering = ("-created_at",)
