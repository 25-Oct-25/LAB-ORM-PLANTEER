from django.urls import path
from . import views
from .views import ( 
    plant_list_view, 
    plant_detail_view, 
    plant_update_view, 
    plant_delete_view, 
    plant_search_view ,
    plants_add_view,
    add_review_view  
)

app_name = 'plants'

urlpatterns = [
    path('all/', plant_list_view, name='plant_list'),
    path('<int:pk>/detail/', plant_detail_view, name='plant_detail'),
    path('<int:pk>/update/', plant_update_view, name='plant_update'),
    path('<int:pk>/delete/', plant_delete_view, name='plant_delete'),
    path('search/', plant_search_view, name='plant_search'),
    path('add/', plants_add_view, name='plants_add_view'),
    path('add/review/<int:plant_id>/', add_review_view, name='add_review_view'),
]