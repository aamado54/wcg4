from django.urls import path

from . import views

app_name = "wcgone_legacy"

urlpatterns = [
    path("", views.home, name="home"),
]
