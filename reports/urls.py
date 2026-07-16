from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("defaults/", views.report_defaults, name="defaults"),
    path("generate/", views.generate_reports, name="generate"),
]
