from django.contrib import admin
from .models import Plant, Comment, Country

# Register your models here.

admin.site.register(Plant)
admin.site.register(Comment)
admin.site.register(Country)