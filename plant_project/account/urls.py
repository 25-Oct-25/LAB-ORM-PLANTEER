from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path("signin/", views.sign_in, name="signin"),
    path("logout/", views.logout_view, name="logout"),

  

    
]
