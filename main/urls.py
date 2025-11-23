# main/urls.py
from django.urls import path, include
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("contact/messages/", views.contact_messages, name="contact_messages"),
    path("", include(("plants.urls", "plants"), namespace="plants")),
]
