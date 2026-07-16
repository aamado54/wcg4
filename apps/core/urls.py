from django.urls import path

from . import views

app_name = "wcgone_core"

urlpatterns = [
    path("importaciones/<int:pk>/", views.import_batch_detail, name="import_batch_detail"),
]
