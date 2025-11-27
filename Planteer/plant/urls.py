from django.urls import path
from . import views

app_name = "plant"

urlpatterns = [
    path("all/", views.all_plants, name="all_plants"),
    path("new/", views.plant_create, name="plant_create"),
    path("<int:plant_id>/detail/", views.plant_detail, name="plant_detail"),
    path("<int:plant_id>/update/", views.plant_update, name="plant_update"),
    path("<int:plant_id>/delete/", views.plant_delete, name="plant_delete"),
    path("search/", views.plant_search, name="plant_search"),
]