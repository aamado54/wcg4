from django.http import HttpResponse


def healthz(_request):
    """Liveness probe for Railway/load balancers (sin BD ni redirect SSL)."""
    return HttpResponse("ok", content_type="text/plain")
