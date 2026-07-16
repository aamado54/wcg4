from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


def splash(request):
    """Landing visual productiva (pgc1); al entrar va al menú principal."""
    return render(request, "splash.html")


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboardhome.html"


@login_required
def dashboard_home(request):
    return render(request, "dashboard/dashboardhome.html")


@login_required
def ayuda(request):
    return render(request, "portal/ayuda.html")
