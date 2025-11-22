#by me 
from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path("all/", views.plant_list, name="all"),                         # /plants/all/
    path("<int:plant_id>/detail/", views.plant_detail, name="detail"),  # /plants/1/detail/
    path("new/", views.plant_create, name="new"),                       # /plants/new/
    path("<int:plant_id>/update/", views.plant_update, name="update"),  # /plants/1/update/
    path("<int:plant_id>/delete/", views.plant_delete, name="delete"),  # /plants/1/delete/
    path("search/", views.plant_search, name="search"),                 # /plants/search/
]
