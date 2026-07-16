from django.shortcuts import redirect


def home(request):
    """Sustituye el stub PGC de wcg_one por el PGC productivo."""
    return redirect("pgc:module_home")
