from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin_view, name='sign_in'),
    path('signup/', views.signup_view, name='sign_up'),
    path('signout/', views.logout_view, name='sign_out'),
]