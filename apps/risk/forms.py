from django import forms

from apps.core.forms import ImportFileForm


class RiskSnapshotImportForm(ImportFileForm):
    fecha_snapshot = forms.DateField(
        required=False,
        label="Fecha de snapshot (opcional)",
        help_text="Si el archivo no trae fecha por fila, use este valor para todas las filas.",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
