from django.shortcuts import redirect


def home(request):
    """Sustituye el placeholder: apunta al PGC real del árbol unificado."""
    return redirect("pgc:module_home")
