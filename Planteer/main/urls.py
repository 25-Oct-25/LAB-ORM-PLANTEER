from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("contact/", views.contact_view, name="contact_view"),    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)