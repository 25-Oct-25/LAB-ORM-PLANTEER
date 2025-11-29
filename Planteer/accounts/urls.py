from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.sign_in, name='sign_in'),
    path('logout/', views.log_out, name='log_out'),
    path("profile/update/", views.update_user_profile, name="update_user_profile"),
    path('profile/<str:user_name>/', views.user_profile_view, name='user_profile'),
    path("my_reviews/", views.my_reviews, name="my_reviews"),
    

]
