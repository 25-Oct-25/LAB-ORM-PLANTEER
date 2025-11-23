from django.urls import path

from . import views


app_name = "plant"

urlpatterns=[
   path('add/',views.add_plant_view,name="add_plant_view"),
   path('all/',views.all_plants_view ,name="all_plants_view"),
   path('detail/<plant_id>/',views.plant_detail_view ,name="plant_detail_view"),
   path('update/<plant_id>/',views.plant_update_view ,name="plant_update_view"),
   path('delete/<plant_id>/',views.plant_delete_view ,name="plant_delete_view"),
   path('contact/',views.send_message_view ,name="send_message_view"),
   path('contact/messages',views.all_messages_view ,name="all_messages_view"),
   path('search/',views.search_plants_view ,name="search_plants_view"),
   path('comment/add/<plant_id>/',views.add_comment_view ,name="add_comment_view"),
]