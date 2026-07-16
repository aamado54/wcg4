from django.urls import path

from . import views

app_name = "wcgone_portal"

urlpatterns = [
    path("panel/", views.PanelView.as_view(), name="panel"),
    path("ayuda/", views.AyudaView.as_view(), name="ayuda"),
    # splash de wcg_one opcional (no es la landing productiva)
    path("splash/", views.SplashView.as_view(), name="splash"),
]
