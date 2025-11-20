from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_plants),
    path('new/', views.create_plant),
    path('<int:plant_id>/detail/', views.plant_detail),
    path('<int:plant_id>/update/', views.update_plant),
    path('<int:plant_id>/delete/', views.delete_plant),
    path('search/', views.search_plants),
]
