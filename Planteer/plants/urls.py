from django.urls import path
from . import views

app_name="plants"

urlpatterns = [
   path('all/', views.plants_all_view, name='plants_all'),
    path('<int:plant_id>/detail/', views.plants_detail_view, name='plants_detail'),
    path('new/', views.plants_new_view, name='plants_new'),
    path('<int:plant_id>/update/', views.plants_update_view, name='plants_update'),
   path('<int:plant_id>/delete/', views.plants_delete_view, name='plants_delete'),
    path('search/', views.plants_search_view, name='plants_search'),
   
]