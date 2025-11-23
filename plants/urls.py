# plants/urls.py
from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path("", views.plant_list, name="all"),
    path("new/", views.plant_create, name="new"),
    path("<int:plant_id>/", views.plant_detail, name="detail"),
    path("<int:plant_id>/update/", views.plant_update, name="update"),
    path("<int:plant_id>/delete/", views.plant_delete, name="delete"),
    path("search/", views.plant_search, name="search"),

    # (اختياري) الخاصة بالدول
    path("country/<str:country_name>/", views.plants_by_country, name="by_country"),
]
