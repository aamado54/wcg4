from django import forms


class ImportFileForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo",
        help_text="Formatos aceptados: CSV o XLSX.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".csv,.xlsx,.xls"}),
    )

    def clean_archivo(self):
        archivo = self.cleaned_data["archivo"]
        name = (archivo.name or "").lower()
        if not name.endswith((".csv", ".xlsx", ".xls", ".txt", ".tsv")):
            raise forms.ValidationError("Use un archivo CSV o XLSX.")
        if archivo.size == 0:
            raise forms.ValidationError("El archivo está vacío.")
        return archivo
