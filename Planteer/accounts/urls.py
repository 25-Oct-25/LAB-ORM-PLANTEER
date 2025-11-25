from django.urls import path
from .views import SignUpView, CustomLoginView, logout_view
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
