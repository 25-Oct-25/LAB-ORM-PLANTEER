# plants/urls.py
from django.urls import path
from . import views

app_name = 'plants'  

urlpatterns = [
    path('all/', views.plant_list_view, name='plant_list'),
    path('<int:plant_id>/detail/', views.plant_detail_view, name='plant_detail'),
    path('new/', views.plant_create_view, name='plant_create'),
    path('<int:plant_id>/update/', views.plant_update_view, name='plant_update'),
    path('<int:plant_id>/delete/', views.plant_delete_view, name='plant_delete'),
    path('search/', views.plant_search_view, name='plant_search'),
]
