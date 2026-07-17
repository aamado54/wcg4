from django import forms

from imports.detection import ALL_IMPORTABLE, TYPE_LABELS


class FileUploadForm(forms.Form):
    stored_file = forms.FileField(label="Archivo a importar")


class GeneralImportForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo",
        help_text="CSV, TSV o Excel (.xlsx). Detección por nombre, estructura y contenido.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )
    tipo_forzado = forms.ChoiceField(
        label="Tipo de importación",
        required=False,
        choices=[("", "— Autodetectar —")] + [(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
        help_text="Obligatorio si la detección es ambigua o de baja confianza.",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
