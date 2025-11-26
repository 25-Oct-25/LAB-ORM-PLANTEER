from django.urls import path
from . import views


app_name = 'plant'

urlpatterns = [
    path("new/", views.create_plant_view , name="create_plant_view"),
    path("all/" , views.all_plants_view ,name="all_plants_view" ),
    path("<plant_id>/detail/" , views.plant_detail_view , name="plant_detail_view" ),
    path("<plant_id>/update/" , views.plant_update_view , name="plant_update_view" ),
    path("search/" , views.plant_search_view , name="plant_search_view" ),
    path("<plant_id>/delete/" , views.plant_delete_view , name="plant_delete_view" ),
    path("<plant_id>/comment/" , views.plant_comment_view , name="plant_comment_view" ),
    path("country/<int:country_id>/", views.plants_country_view, name="plants_country_view"),

 ]