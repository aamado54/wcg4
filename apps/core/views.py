from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from apps.core.models import DataImportBatch, DataImportError


@login_required
def import_batch_detail(request, pk):
    batch = get_object_or_404(
        DataImportBatch.objects.select_related("usuario"),
        pk=pk,
    )
    errores = batch.errores.all()[:200]
    context = {
        "batch": batch,
        "errores": errores,
        "breadcrumbs": [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Importaciones"},
            {"label": f"Lote #{batch.pk}"},
        ],
    }
    return render(request, "wcgone/imports/batch_result.html", context)
