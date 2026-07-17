from django import forms

from imports.detection import ALL_IMPORTABLE, TYPE_LABELS


class FileUploadForm(forms.Form):
    stored_file = forms.FileField(label="Archivo a importar")


class GeneralImportForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo",
        help_text="CSV, TSV o Excel (.xlsx). El sistema detecta el tipo por nombre y columnas.",
    )
    tipo_forzado = forms.ChoiceField(
        label="Tipo (opcional)",
        required=False,
        choices=[("", "— Autodetectar —")] + [(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
        help_text="Use solo si la autodetección no es confiable.",
    )
