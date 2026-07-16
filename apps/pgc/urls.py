from django.urls import path

from . import views

app_name = "wcgone_pgc"

urlpatterns = [
    path("", views.home, name="home"),
]
