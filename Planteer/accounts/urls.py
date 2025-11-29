from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile_update_view, user_profile_view

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/update/', profile_update_view, name='profile_update_view'),
    path('profile/<str:user_name>/', user_profile_view, name='user_profile_view'), 
]