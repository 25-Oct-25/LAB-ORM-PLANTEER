from django.urls import path
from . import views

app_name="plants"

urlpatterns = [
  path('plants/all/', views.plants_view, name='plants_view'),
  path('plants/<plant_id>/detail/', views.plant_details_view, name='plant_details_view'),
  path('plants/new/', views.add_plant_view, name='add_plant_view'),
  path('plants/<plant_id>/update/', views.update_plant_view, name='update_plant_view'),
  path('plants/<plant_id>/delete/', views.delete_plant, name='delete_plant'),
  path('plants/search/', views.search_view, name='search_view'),

]