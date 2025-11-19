from django.urls import path
from .views import ( 
    plant_list_view, 
    plant_detail_view, 
    plant_create_view, 
    plant_update_view, 
    plant_delete_view, 
    plant_search_view 
)

app_name = 'plants'

urlpatterns = [
    path('all/', plant_list_view, name='plant_list'),
    path('<int:pk>/detail/', plant_detail_view, name='plant_detail'),
    path('new/', plant_create_view, name='plant_create'),
    path('<int:pk>/update/', plant_update_view, name='plant_update'),
    path('<int:pk>/delete/', plant_delete_view, name='plant_delete'),
    path('search/', plant_search_view, name='plant_search'),
]