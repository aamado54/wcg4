from django.urls import path

from . import views

app_name = "portal"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path("ayuda/", views.ayuda, name="ayuda"),
]
