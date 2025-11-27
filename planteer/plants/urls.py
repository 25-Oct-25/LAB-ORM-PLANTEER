from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('all/', views.plant_list, name='plant_list'),
    path('<int:plant_id>/detail/', views.plant_detail, name='plant_detail'),
    path('new/', views.plant_create, name='plant_create'),
    path('<int:plant_id>/update/', views.plant_update, name='plant_update'),
    path('<int:plant_id>/delete/', views.plant_delete, name='plant_delete'),
    path('search/', views.plant_search_view, name='plant_search'),
    
    path('country/<int:country_id>/', views.country_detail, name='country_detail'), 
]   