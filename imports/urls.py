from django.urls import path
from . import views

app_name = "imports"

urlpatterns = [
    path("", views.import_hub, name="import_hub"),
    path("<int:file_id>/process-new-clients/", views.process_new_clients, name="process_new_clients"),
    path("<int:file_id>/process-cross-sale/", views.process_cross_sale, name="process_cross_sale"),
    path("<int:file_id>/process-station-times/", views.process_station_times, name="process_station_times"),
]
